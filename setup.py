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
    long_description='\r\n# More Logs - Structured Logging and Exception Handling\r\n\r\n\r\n|Branch      |Status   |\r\n|------------|---------|\r\n|master      | [![Build Status](https://travis-ci.org/klahnakoski/mo-logs.svg?branch=master)](https://travis-ci.org/klahnakoski/mo-logs) |\r\n|dev         | [![Build Status](https://travis-ci.org/klahnakoski/mo-logs.svg?branch=dev)](https://travis-ci.org/klahnakoski/mo-logs)  [![Coverage Status](https://coveralls.io/repos/github/klahnakoski/mo-logs/badge.svg?branch=dev)](https://coveralls.io/github/klahnakoski/mo-logs?branch=dev)  |\r\n\r\n\r\nThis library provides two main features\r\n\r\n* **Structured logging** - output is all JSON (with options to serialize to text for humans)\r\n* **Exception handling weaved in** - Good logs must represent what happened,\r\nand that can only be done if the logging library is intimately familiar with\r\nthe (exceptional) code paths taken.\r\n\r\n## Motivation\r\n\r\nException handling and logging are undeniably linked. There are many instances\r\nwhere exceptions are raised and must be logged, and others where the subsuming \r\nsystem can fully handle the exception, and no log should be emitted. Exception \r\nhandling semantics are great because they decouple the cause from the solution, \r\nbut this can be at odds with clean logging - which couples raising and catching \r\nto make appropriate decisions about what to emit to the log.  \r\n\r\nThis logging module is additionally responsible for raising exceptions,\r\ncollecting the trace and context, and then deducing if it must be logged, or\r\nif it can be ignored because something can handle it.\r\n\r\n\r\n## Basic Usage\r\n\r\n### Use `Log.note()` for all logging\r\n\r\n```python\r\n    Log.note("Hello, World!")\r\n```\r\n\r\nThere is no need to create logger objects. The `Log` module will keep track of\r\nwhat, where and when of every call.\r\n\r\n### Using named parameters\r\n\r\nAll logging calls accept a string template with named parameters. Keyword arguments\r\ncan be added to the call to provide values. The template and arguments are not \r\ncombined at call time, rather they are held in a JSON-izable data structure for \r\nstructured logging. The template is only expanded *if* the log is serialized for humans.  \r\n\r\n```python\r\n    Log.note("Hello, {{name}}!", name="World!")\r\n```\r\n\r\n**Do not use Python\'s string formatting features:**\r\n \r\n* [string formatting operator (`%`)](http://python-reference.readthedocs.io/en/latest/docs/str/formatting.html), \r\n* [the `format()` function](https://docs.python.org/3/library/stdtypes.html#str.format) \r\n* [literal string intrpolation](https://www.python.org/dev/peps/pep-0498/).\r\n\r\nUsing any of these will expand the string template at call time, which is a parsing\r\nnightmare for log analysis tools.\r\n\r\n\r\n### Parametric parameters\r\n\r\nAll the `Log` functions accept a `default_params` as a second parameter, like so:\r\n\r\n```python\r\n    Log.note("Hello, {{name}}!", {"name": "World!"})\r\n```\r\n\r\nthis is meant for the situation your code already has a bundled structure you\r\nwish to use as a source of parameters. If keyword parameters are used, they\r\nwill override the default values. Be careful when sending whole data\r\nstructures, they will be logged!\r\n\r\n### Formatting parameters\r\n\r\nThere are a variety of formatters, and they can be applied by using the \r\npipe (`|`) symbol.  \r\n\r\nIn this example we cast the `name` to uppercase\r\n\r\n```python\r\n    Log.note("Hello, {{name|upper}}!", name="World!")\r\n```\r\n\r\nSome formatters accept arguments:\r\n\r\n```python\r\n    Log.note("pi is {{pi|round(places=3)}}!", pi=3.14159265)\r\n```\r\n\r\nYou can look at the [`strings` module](https://github.com/klahnakoski/mo-logs/blob/dev/mo_logs/strings.py#L56) to see the formatters available.\r\n\r\n### Please, never use locals()\r\n\r\n```python\r\n    def worker(value):\r\n        name = "tout le monde!"\r\n        password = "123"\r\n        Log.note("Hello, {{name}}", locals())      # DO NOT DO THIS!\r\n```\r\n\r\nDespite the fact using `locals()` is a wonderful shortcut for logging it is\r\ndangerous because it also picks up sensitive local variables. Even if\r\n`{{name}}` is the only value in the template, the whole `locals()` dict will\r\nbe sent to the structured loggers for recording. \r\n\r\n### Destination: Database!\r\n\r\nAll logs are structured logs; the parameters will be included, unchanged, in\r\nthe log structure. This library also expects all parameter values to be JSON-\r\nserializable so they can be stored/processed by downstream JSON tools.\r\n\r\n**Example structured log** \r\n```json\r\n    {\r\n        "template": "Hello, {{name}}!",\r\n        "params": {"name": "World!"},\r\n        "context": "NOTE",\r\n        "format": "{{machine.name}} (pid {{machine.pid}}) - {{timestamp|datetime}} - {{thread.name}} - \\"{{location.file}}:{{location.line}}\\" - ({{location.method}}) - Hello, {{params.name}}!",\r\n        "location": {\r\n            "file": "/home/kyle/code/example.py",\r\n            "line": 10,\r\n            "method": "worker"\r\n        },\r\n        "machine": {\r\n            "name": "klahnakoski-39477",\r\n            "os": "Windows10",\r\n            "pid": 18060,\r\n            "python": "CPython"\r\n        },\r\n        "thread": {\r\n            "id": 14352,\r\n            "name": "Main Thread"\r\n        },\r\n        "timestamp": 1578673471\r\n    }\r\n```\r\n\r\n## Exception Handling\r\n\r\n### Instead of `raise` use `Log.error()`\r\n\r\n```python\r\n    Log.error("This will throw an error")\r\n```\r\n\r\nThe actual call will always raise an exception, and it manipulates the stack\r\ntrace to ensure the caller is appropriately blamed. Feel free to use the\r\n`raise` keyword (as in `raise Log.error("")`), if that looks nicer to you. \r\n\r\n### Always chain your exceptions\r\n\r\nThe `cause` parameter accepts an `Exception`, or a list of exceptions.\r\nChaining is generally good practice that helps you find the root cause of\r\na failure. \r\n\r\n```python\r\n    try:\r\n        # Do something that might raise exception\r\n    except Exception as e:\r\n        Log.error("Describe what you were trying to do", cause=e)\r\n```\r\n\r\n### Use named parameters in your error descriptions too\r\n\r\nError logging accepts keyword parameters just like `Log.note()` does\r\n\r\n```python\r\n    def worker(value):\r\n        try:\r\n            Log.note("Start working with {{key1}}", key1=value1)\r\n            # Do something that might raise exception\r\n        except Exception as e:\r\n            Log.error("Failure to work with {{key2}}", key2=value2, cause=e)\r\n```\r\n\r\n### No need to formally type your exceptions\r\n\r\nAn exception can be uniquely identified by the message template\r\nit is given; exceptions raised with the same template are the same type. You\r\nshould have no need to create new exception types.\r\n\r\n### Testing for exception "types"\r\n\r\nThis library advocates chaining exceptions early and often, and this hides\r\nimportant exception types in a long causal chain. `mo-logs` allows you to easily\r\ntest if a type (or string, or template) can be found in the causal chain by using\r\nthe `in` keyword:   \r\n\r\n```python\r\n    def worker(value):\r\n        try:\r\n            # Do something that might raise exception\r\n        except Exception as e:\r\n            if "Failure to work with {{key2}}" in e:\r\n                # Deal with exception thrown in above code, no matter\r\n                # how many other exception handlers were in the chain\r\n```\r\n\r\nFor those who may abhor the use of magic strings, feel free to use constants instead:\r\n\r\n```python\r\n    KEY_ERROR = "Failure to work with {{key}}"\r\n\r\n    try:\r\n        Log.error(KEY_ERROR, key=42)        \r\n    except Exception as e:\r\n        if KEY_ERROR in e:\r\n            Log.note("dealt with key error")\r\n```\r\n\r\n\r\n\r\n\r\n### If you can deal with an exception, then it will never be logged\r\n\r\nWhen a caller catches an exception from a callee, it is the caller\'s\r\nresponsibility to handle that exception, or re-raise it. There are many\r\nsituations a caller can be expected to handle exceptions; and in those cases\r\nlogging an error would be deceptive. \r\n\r\n```python\r\n    def worker(value):\r\n        try:\r\n            Log.error("Failure to work with {{key3}}", key3=value3)\r\n        except Exception as e:\r\n            # Try something else\r\n```\r\n\r\n### Use `Log.warning()` if your code can deal with an exception, but you still want to log it as an issue\r\n\r\n```python\r\n    def worker(value):\r\n        try:\r\n            Log.note("Start working with {{key4}}", key4=value4)\r\n            # Do something that might raise exception\r\n        except Exception as e:\r\n            Log.warning("Failure to work with {{key4}}", key4=value4, cause=e)\r\n```\r\n### Don\'t loose your stack trace!\r\n\r\nBe aware your `except` clause can also throw exceptions: In the event you\r\ncatch a vanilla Python Exception, you run the risk of loosing its stack trace.\r\nTo prevent this, wrap your exception in an `Except` object, which will capture\r\nyour trace for later use. Exceptions thrown from this `Log` library need not\r\nbe wrapped because they already captured their trace. If you wrap an `Except`\r\nobject, you simply get back the object you passed.\r\n\r\n\r\n```python\r\n    try:\r\n        # DO SOME WORK        \r\n    except Exception as e:\r\n        e = Except.wrap(e)\r\n        # DO SOME FANCY ERROR RECOVERY\r\n ```\r\n\r\n### Always catch all `Exceptions`\r\n\r\nCatching all exceptions is preferred over the *only-catch-what-you-can-handle*\r\nstrategy. First, exceptions are not lost because we are chaining. Second,\r\nwe catch unexpected `Exceptions` early and we annotate them with a\r\ndescription of what the local code was intending to do. This annotation\r\neffectively groups the possible errors (known, or not) into a class, which\r\ncan be used by callers to decide on appropriate mitigation.  \r\n\r\nTo repeat: When using dependency injection, callers can not reasonably be\r\nexpected to know about the types of failures that can happen deep down the\r\ncall chain. This makes it vitally important that methods summarize all\r\nexceptions, both known and unknown, so their callers have the information to\r\nmake better decisions on appropriate action.  \r\n\r\nFor example: An abstract document container, implemented on top of a SQL \r\ndatabase, should not emit SQLExceptions of any kind: A caller that uses a \r\ndocument container should not need to know how to handle SQLExceptions (or any \r\nother implementation-specific exceptions). Rather, in this example, the \r\ncaller should be told it "can not add a document", or "can not remove a \r\ndocument". This allows the caller to make reasonable decisions when they do \r\noccur. The original cause (the SQLException) is in the causal chain.\r\n\r\nAnother example, involves *nested exceptions*: If you catch a particular type \r\nof exception, you may inadvertently catch the same type of exception \r\nfrom deeper in the call chain. Narrow exception handling is an illusion. \r\nBroad exception handling will force you to consider a variety of failures \r\nearly; force you to consider what it means when a block of code fails; and \r\nforce you to describe it for others.\r\n\r\n### Don\'t make methods you do not need\r\n\r\nThere is an argument that suggests you should break your code into logical methods, rather than catching exceptions: The method name will describe action that failed, and the stack trace can be inspected to make mitigation decisions. Additional methods is a poor solution:\r\n\r\n* More methods means more complexity; the programmer must find the method, remember the method, and wonder if the method is used elsewhere.\r\n* Methods can be removed while refactoring; exceptions make it clear the error is important\r\n* Compiler optimizations can interfere with the call stack\r\n* The method name is not an appropriate description of the problem: Many words may be required for clarity.\r\n* Code that inspects its own stack trace is messy code.\r\n* A stack trace does not include runtime values that are vital for describing the problem.\r\n\r\n\r\n## Log \'Levels\'\r\n\r\nThe `mo-logs` module has no concept of logging levels it is expected that debug\r\nvariables (variables prefixed with `DEBUG_` are used to control the logging\r\noutput.\r\n\r\n\r\n```python\r\n    # simple.py\r\n    DEBUG_SHOW_DETAIL = True\r\n\r\n    def worker():\r\n        if DEBUG_SHOW_DETAIL:\r\n            Log.note("Starting")\r\n\r\n        # DO WORK HERE\r\n\r\n        if DEBUG_SHOW_DETAIL:\r\n            Log.note("Done")\r\n\r\n    def main():\r\n        try:\r\n            settings = startup.read_settings()\r\n            Log.start(settings.debug)\r\n\r\n            # DO WORK HERE\r\n\r\n        except Exception as e:\r\n            Log.error("Complain, or not", e)\r\n        finally:\r\n            Log.stop()\r\n```\r\n\r\nThis pattern of using explict debug variables allows the programmer to switch logging on and off on individual subsystems that share that variable: Either multiple debug variables in a single module, or multiple modules sharing a single debug variable.\r\n\r\nThese debug variables can be switched on/off by configuration file:\r\n\r\n```javascript\r\n    // settings.json\r\n    {\r\n        "debug":{\r\n            "constants":{"simple.DEBUG_SHOW_DETAILS":false}\r\n        }\r\n    }\r\n```\r\n\r\nTo keep logging to a single line, you may consider this pattern:\r\n\r\n    DEBUG and Log.note("error: {{value}}", value=expensive_function()) \r\n\r\nNotice the `expensive_function()` is not run when `DEBUG` is false.\r\n\r\n## Log Configuration\r\n\r\nThe `mo-logs` library will log to the console by default. ```Log.start(settings)```\r\nwill redirect the logging to other streams, as defined by the settings:\r\n\r\n *  **log** - List of all log-streams and their parameters\r\n *  **trace** - Show more details in every log line (default False)\r\n *  **cprofile** - Used to enable the builtin python c-profiler, ensuring the cprofiler is turned on for all spawned threads. (default False)\r\n *  **constants** - Map absolute path of module constants to the values that will be assigned. Used mostly to set debugging constants in modules.\r\n\r\nOf course, logging should be the first thing to be setup (aside from digesting\r\nsettings of course). For this reason, applications should have the following\r\nstructure:\r\n\r\n```python\r\n    def main():\r\n        try:\r\n            settings = startup.read_settings()\r\n            Log.start(settings.debug)\r\n\r\n            # DO WORK HERE\r\n\r\n        except Exception as e:\r\n            Log.error("Complain, or not", e)\r\n        finally:\r\n            Log.stop()\r\n```\r\n\r\nExample configuration file\r\n\r\n```json\r\n{\r\n    "log": [\r\n        {\r\n            "class": "logging.handlers.RotatingFileHandler",\r\n            "filename": "examples/logs/examples_etl.log",\r\n            "maxBytes": 10000000,\r\n            "backupCount": 100,\r\n            "encoding": "utf8"\r\n        },\r\n        {\r\n            "log_type": "email",\r\n            "from_address": "klahnakoski@mozilla.com",\r\n            "to_address": "klahnakoski@mozilla.com",\r\n            "subject": "[ALERT][DEV] Problem in ETL Spot",\r\n            "$ref": "file://~/private.json#email"\r\n        },\r\n        {\r\n            "log_type": "console"\r\n        }\r\n    ]\r\n}\r\n```\r\n\r\n## Capturing logs\r\n\r\nYou can capture all the logging message and send them to your own logging with \r\n\r\n    Log.set_logger(myLogger)\r\n    \r\nwhere `myLogger` is an instance that can accept a calls to `write(template, parameters)`. If your logging library can only handle strings, then use `message = expand_template(template, params)`.\r\n\r\n\r\n## Problems with Python Logging\r\n\r\n[Python\'s default `logging` module](https://docs.python.org/2/library/logging.html#logging.debug)\r\ncomes close to doing the right thing, but fails:  \r\n\r\n  * It has keyword parameters, but they are expanded at call time so the values are lost in a string.  \r\n  * It has `extra` parameters, but they are lost if not used by the matching `Formatter`.  \r\n  * It even has stack trace with `exc_info` parameter, but only if an exception is being handled.\r\n  * Python 2.x has no builtin exception chaining, but [Python 3 does](https://www.python.org/dev/peps/pep-3134/)\r\n\r\n### More Reading\r\n\r\n* **Structured Logging is Good** - https://sites.google.com/site/steveyegge2/the-emacs-problem\r\n\r\n',
    long_description_content_type='text/markdown',
    name='mo-logs',
    packages=["mo_logs"],
    url='https://github.com/klahnakoski/mo-logs',
    version='3.64.20113',
    zip_safe=False
)