# encoding: utf-8
# THIS FILE IS AUTOGENERATED!
from __future__ import unicode_literals
from setuptools import setup
setup(
    author='Kyle Lahnakoski',
    author_email='kyle@lahnakoski.com',
    classifiers=["Development Status :: 4 - Beta","Topic :: Software Development :: Libraries","Topic :: Software Development :: Libraries :: Python Modules","License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)","Programming Language :: Python :: 2.7","Programming Language :: Python :: 3.6"],
    description='More Logs! Structured Logging and Exception Handling',
    include_package_data=True,
    install_requires=["mo-dots>=3.63.20108","mo-future>=3.51.20059"],
    license='MPL 2.0',
    long_description='\n# More Logs - Structured Logging and Exception Handling\n\n\n|Branch      |Status   |\n|------------|---------|\n|master      | [![Build Status](https://travis-ci.org/klahnakoski/mo-logs.svg?branch=master)](https://travis-ci.org/klahnakoski/mo-logs) |\n|dev         | [![Build Status](https://travis-ci.org/klahnakoski/mo-logs.svg?branch=dev)](https://travis-ci.org/klahnakoski/mo-logs)  [![Coverage Status](https://coveralls.io/repos/github/klahnakoski/mo-logs/badge.svg?branch=dev)](https://coveralls.io/github/klahnakoski/mo-logs?branch=dev)  |\n\n\nThis library provides two main features\n\n* **Structured logging** - output is all JSON (with options to serialize to text for humans)\n* **Exception handling weaved in** - Good logs must represent what happened,\nand that can not be done if the logging library is not intimately familiar with\nthe (exceptional) code paths taken.\n\n## Motivation\n\nException handling and logging are undeniably linked. There are many instances\nwhere exceptions are raised and must be logged, and others where the subsuming \nsystem can fully handle the exception, and no log should be emitted. Exception \nhandling semantics are great because they decouple the cause from the solution, \nbut this can be at odds with clean logging - which couples raising and catching \nto make appropriate decisions about what to emit to the log.  \n\nThis logging module is additionally responsible for raising exceptions,\ncollecting the trace and context, and then deducing if it must be logged, or\nif it can be ignored because something can handle it.\n\n\n## Basic Usage\n\n### Use `Log.note()` for all logging\n\n```python\n    Log.note("Hello, World!")\n```\n\nThere is no need to create logger objects. The `Log` module will keep track of\nwhat, where and when of every call.\n\n### Using named parameters\n\nAll logging calls accept a string template with named parameters. Keyword arguments\ncan be added to the call to provide values. The template and arguments are not \ncombined at call time, rather they are held in a JSON-izable data structure for \nstructured logging. The template is only expanded *if* the log is serialized for humans.  \n\n```python\n    Log.note("Hello, {{name}}!", name="World!")\n```\n\n**Do not use Python\'s string formatting features:**\n \n* [string formatting operator (`%`)](http://python-reference.readthedocs.io/en/latest/docs/str/formatting.html), \n* [the `format()` function](https://docs.python.org/3/library/stdtypes.html#str.format) \n* [literal string intrpolation](https://www.python.org/dev/peps/pep-0498/).\n\nUsing any of these will expand the string template at call time, which is a parsing\nnightmare for log analysis tools.\n\n\n### Parametric parameters\n\nAll the `Log` functions accept a `default_params` as a second parameter, like so:\n\n```python\n    Log.note("Hello, {{name}}!", {"name": "World!"})\n```\n\nthis is meant for the situation your code already has a bundled structure you\nwish to use as a source of parameters. If keyword parameters are used, they\nwill override the default values. Be careful when sending whole data\nstructures, they will be logged!\n\n### Formatting parameters\n\nThere are a variety of formatters, and they can be applied by using the \npipe (`|`) symbol.  \n\nIn this example we cast the `name` to uppercase\n\n```python\n    Log.note("Hello, {{name|upper}}!", name="World!")\n```\n\nSome formatters accept arguments:\n\n```python\n    Log.note("pi is {{pi|round(places=3)}}!", pi=3.14159265)\n```\n\nYou can look at the [`strings` module](https://github.com/klahnakoski/mo-logs/blob/dev/mo_logs/strings.py#L56) to see the formatters available.\n\n### Please, never use locals()\n\n```python\n    def worker(value):\n        name = "tout le monde!"\n        password = "123"\n        Log.note("Hello, {{name}}", locals())      # DO NOT DO THIS!\n```\n\nDespite the fact using `locals()` is a wonderful shortcut for logging it is\ndangerous because it also picks up sensitive local variables. Even if\n`{{name}}` is the only value in the template, the whole `locals()` dict will\nbe sent to the structured loggers for recording. \n\n### Destination: Database!\n\nAll logs are structured logs; the parameters will be included, unchanged, in\nthe log structure. This library also expects all parameter values to be JSON-\nserializable so they can be stored/processed by downstream JSON tools.\n\n**Example structured log** \n```json\n    {\n        "template": "Hello, {{name}}!",\n        "params": {"name": "World!"},\n        "context": "NOTE",\n        "format": "{{machine.name}} (pid {{machine.pid}}) - {{timestamp|datetime}} - {{thread.name}} - \\"{{location.file}}:{{location.line}}\\" - ({{location.method}}) - Hello, {{params.name}}!",\n        "location": {\n            "file": "/home/kyle/code/example.py",\n            "line": 10,\n            "method": "worker"\n        },\n        "machine": {\n            "name": "klahnakoski-39477",\n            "os": "Windows10",\n            "pid": 18060,\n            "python": "CPython"\n        },\n        "thread": {\n            "id": 14352,\n            "name": "Main Thread"\n        },\n        "timestamp": 1578673471\n    }\n```\n\n## Exception Handling\n\n### Instead of `raise` use `Log.error()`\n\n```python\n    Log.error("This will throw an error")\n```\n\nThe actual call will always raise an exception, and it manipulates the stack\ntrace to ensure the caller is appropriately blamed. Feel free to use the\n`raise` keyword (as in `raise Log.error("")`), if that looks nicer to you. \n\n### Always chain your exceptions\n\nThe `cause` parameter accepts an `Exception`, or a list of exceptions.\nChaining is generally good practice that helps you find the root cause of\na failure. \n\n```python\n    try:\n        # Do something that might raise exception\n    except Exception as e:\n        Log.error("Describe what you were trying to do", cause=e)\n```\n\n### Use named parameters in your error descriptions too\n\nError logging accepts keyword parameters just like `Log.note()` does\n\n```python\n    def worker(value):\n        try:\n            Log.note("Start working with {{key1}}", key1=value1)\n            # Do something that might raise exception\n        except Exception as e:\n            Log.error("Failure to work with {{key2}}", key2=value2, cause=e)\n```\n\n### No need to formally type your exceptions\n\nAn exception can be uniquely identified by the first-parameter string template\nit is given; exceptions raised with the same template are the same type. You\nshould have no need to create new exception types.\n\n### Testing for exception "types"\n\nThis library advocates chaining exceptions early and often, and this hides\nimportant exception types in a long causal chain. `mo-logs` allows you to easily\ntest if a type (or string, or template) can be found in the causal chain by using\nthe `in` keyword:   \n\n```python\n    def worker(value):\n        try:\n            # Do something that might raise exception\n        except Exception as e:\n            if "Failure to work with {{key2}}" in e:\n                # Deal with exception thrown in above code, no matter\n                # how many other exception handlers were in the chain\n```\n\nFor those who may abhor the use of magic strings, feel free to use constants instead:\n\n```python\n    KEY_ERROR = "Failure to work with {{key}}"\n\n    try:\n        Log.error(KEY_ERROR, key=42)        \n    except Exception as e:\n        if KEY_ERROR in e:\n            Log.note("dealt with key error")\n```\n\n\n\n\n### If you can deal with an exception, then it will never be logged\n\nWhen a caller catches an exception from a callee, it is the caller\'s\nresponsibility to handle that exception, or re-raise it. There are many\nsituations a caller can be expected to handle exceptions; and in those cases\nlogging an error would be deceptive. \n\n```python\n    def worker(value):\n        try:\n            Log.error("Failure to work with {{key3}}", key3=value3)\n        except Exception as e:\n            # Try something else\n```\n\n### Use `Log.warning()` if your code can deal with an exception, but you still want to log it as an issue\n\n```python\n    def worker(value):\n        try:\n            Log.note("Start working with {{key4}}", key4=value4)\n            # Do something that might raise exception\n        except Exception as e:\n            Log.warning("Failure to work with {{key4}}", key4=value4, cause=e)\n```\n### Don\'t loose your stack trace!\n\nBe aware your `except` clause can also throw exceptions: In the event you\ncatch a vanilla Python Exception, you run the risk of loosing its stack trace.\nTo prevent this, wrap your exception in an `Except` object, which will capture\nyour trace for later use. Exceptions thrown from this `Log` library need not\nbe wrapped because they already captured their trace. If you wrap an `Except`\nobject, you simply get back the object you passed.\n\n\n```python\n    try:\n        # DO SOME WORK        \n    except Exception as e:\n        e = Except.wrap(e)\n        # DO SOME FANCY ERROR RECOVERY\n ```\n\n### Always catch all `Exceptions`\n\nCatching all exceptions is preferred over the *only-catch-what-you-can-handle*\nstrategy. First, exceptions are not lost because we are chaining. Second,\nwe catch unexpected `Exceptions` early and we annotate them with a\ndescription of what the local code was intending to do. This annotation\neffectively groups the possible errors (known, or not) into a class, which\ncan be used by callers to decide on appropriate mitigation.  \n\nTo repeat: When using dependency injection, callers can not reasonably be\nexpected to know about the types of failures that can happen deep down the\ncall chain. This makes it vitally important that methods summarize all\nexceptions, both known and unknown, so their callers have the information to\nmake better decisions on appropriate action.  \n\nFor example: An abstract document container, implemented on top of a SQL \ndatabase, should not emit SQLExceptions of any kind: A caller that uses a \ndocument container should not need to know how to handle SQLExceptions (or any \nother implementation-specific exceptions). Rather, in this example, the \ncaller should be told it "can not add a document", or "can not remove a \ndocument". This allows the caller to make reasonable decisions when they do \noccur. The original cause (the SQLException) is in the causal chain.\n\nAnother example, involves *nested exceptions*: If you catch a particular type \nof exception, you may inadvertently catch the same type of exception \nfrom deeper in the call chain. Narrow exception handling is an illusion. \nBroad exception handling will force you to consider a variety of failures \nearly; force you to consider what it means when a block of code fails; and \nforce you to describe it for others.\n\n### Don\'t make methods you do not need\n\nThere is an argument that suggests you should break your code into logical methods, rather than catching exceptions: The method name will describe action that failed, and the stack trace can be inspected to make mitigation decisions. Additional methods is a poor solution:\n\n* More methods means more complexity; the programmer must find the method, remember the method, and wonder if the method is used elsewhere.\n* Methods can be removed while refactoring; exceptions make it clear the error is important\n* Compiler optimizations can interfere with the call stack\n* The method name is not an appropriate description of the problem: May words may be required for clarity.\n* Inspecting stack traces makes for messy code.\n* A stack trace does not include runtime values that are vital for describing the problem.\n\n\n## Log \'Levels\'\n\nThe `mo-logs` module has no concept of logging levels it is expected that debug\nvariables (variables prefixed with `DEBUG_` are used to control the logging\noutput.\n\n\n```python\n    # simple.py\n    DEBUG_SHOW_DETAIL = True\n\n    def worker():\n        if DEBUG_SHOW_DETAIL:\n            Log.note("Starting")\n\n        # DO WORK HERE\n\n        if DEBUG_SHOW_DETAIL:\n            Log.note("Done")\n\n    def main():\n        try:\n            settings = startup.read_settings()\n            Log.start(settings.debug)\n\n            # DO WORK HERE\n\n        except Exception as e:\n            Log.error("Complain, or not", e)\n        finally:\n            Log.stop()\n```\n\nThis pattern of using explict debug variables allows the programmer to switch logging on and off on individual subsystems that share that variable: Either multiple debug variables in a single module, or multiple modules sharing a single debug variable.\n\nThese debug variables can be switched on/off by configuration file:\n\n```javascript\n    // settings.json\n    {\n        "debug":{\n            "constants":{"simple.DEBUG_SHOW_DETAILS":false}\n        }\n    }\n```\n\nTo keep logging to a single line, you may consider this pattern:\n\n    DEBUG and Log.note("error: {{value}}", value=expensive_function()) \n\nNotice the `expensive_function()` is not run when `DEBUG` is false.\n\n## Log Configuration\n\nThe `mo-logs` library will log to the console by default. ```Log.start(settings)```\nwill redirect the logging to other streams, as defined by the settings:\n\n *  **log** - List of all log-streams and their parameters\n *  **trace** - Show more details in every log line (default False)\n *  **cprofile** - Used to enable the builtin python c-profiler, ensuring the cprofiler is turned on for all spawned threads. (default False)\n *  **constants** - Map absolute path of module constants to the values that will be assigned. Used mostly to set debugging constants in modules.\n\nOf course, logging should be the first thing to be setup (aside from digesting\nsettings of course). For this reason, applications should have the following\nstructure:\n\n```python\n    def main():\n        try:\n            settings = startup.read_settings()\n            Log.start(settings.debug)\n\n            # DO WORK HERE\n\n        except Exception as e:\n            Log.error("Complain, or not", e)\n        finally:\n            Log.stop()\n```\n\nExample configuration file\n\n```json\n{\n    "log": [\n        {\n            "class": "logging.handlers.RotatingFileHandler",\n            "filename": "examples/logs/examples_etl.log",\n            "maxBytes": 10000000,\n            "backupCount": 100,\n            "encoding": "utf8"\n        },\n        {\n            "log_type": "email",\n            "from_address": "klahnakoski@mozilla.com",\n            "to_address": "klahnakoski@mozilla.com",\n            "subject": "[ALERT][DEV] Problem in ETL Spot",\n            "$ref": "file://~/private.json#email"\n        },\n        {\n            "log_type": "console"\n        }\n    ]\n}\n```\n\n## Capturing logs\n\nYou can capture all the logging message and send them to your own logging with \n\n    Log.set_logger(myLogger)\n    \nwhere `myLogger` is an instance that can accept a calls to `write(template, parameters)`. If your logging library can only handle strings, then use `message = expand_template(template, params)`.\n\n\n## Problems with Python Logging\n\n[Python\'s default `logging` module](https://docs.python.org/2/library/logging.html#logging.debug)\ncomes close to doing the right thing, but fails:  \n\n  * It has keyword parameters, but they are expanded at call time so the values are lost in a string.  \n  * It has `extra` parameters, but they are lost if not used by the matching `Formatter`.  \n  * It even has stack trace with `exc_info` parameter, but only if an exception is being handled.\n  * Python 2.x has no builtin exception chaining, but [Python 3 does](https://www.python.org/dev/peps/pep-3134/)\n\n### More Reading\n\n* **Structured Logging is Good** - https://sites.google.com/site/steveyegge2/the-emacs-problem\n\n',
    long_description_content_type='text/markdown',
    name='mo-logs',
    packages=["mo_logs"],
    url='https://github.com/klahnakoski/mo-logs',
    version='3.63.20108',
    zip_safe=False
)