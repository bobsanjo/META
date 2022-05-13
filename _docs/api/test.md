---
permalink: /docs/api/test/
title: "test()"
---

```python
test(...)
```

MetaBuild allows users to define unit tests and run them through the [metabuild test]({{ site.baseurl }}{% link _docs/cli/metabuild_test.md %}) CLI command (after running `metabuild prepare` and `metabuild build`).
A `test()` enables running unit tests through a python function. As with the `genrule()` the python method can call `invoke` through the `context` parameter to run a binary.
Inherits all attributes from [Genrule]({{ site.baseurl }}{% link _docs/api/genrule.md %})
The following attributes are specific to `Genrule` and should not be used: `exec`, `cmd`, `env`, `environment_expansion_separator`, `inputs`. 
The most useful attributes can be found in the table below:

| Attribute | Type | Description |
|-----------|------|-------------|
| `py` | [`<py method>`]({{ site.baseurl }}{% link _docs/guides/py_method.md %}) | The generation rule specified as a Python method. |
| `env` | `dict` | Dictionary containing the environment variables used . |
| `deps` | `list` | List of dependencies that are used to run the test. |
| `labels` | `list` | List of labels that can be used to filter the test. |

## Example:

```py

cxx_library(
    name = "lib1",
    srcs = [
        "lib1.cpp"
    ],
    tests = [
        ":lib1_test1"
    ]
)

async def _run_lib1_test(context):
    gtest_report_path_arg = "--gtest_output=xml:" + ctx.inputs[0]
    res, output, _ = await context.invoke(":lib1_test_exe", args=["test_arg1", "test_arg2", gtest_report_path_arg])
    test_results = context.parse_report_file("junit", gtest_report_path)
    for test_result in test_results:
        context.report_test_result(test_result)

test(
    name = "lib1_test1",
    deps = ":lib1_test_exe",
    py = _run_lib1_test,
    labels = ["smoke"],
    outputs = [
        # The file will be created at the output location of this node
        # for the corresponding target_config (release, debug, ..) in the build folder.
        "gtest_report.xml",
    ],
)

cxx_binary(
    name = "lib1_test_exe",
    srcs = "lib1.test.cpp",
    deps = [
        ":lib1",
    ]
)

```

For more detailed examples of using the `test()` node see the [tests_app](https://git.corp.adobe.com/meta-build/meta-build/tree/main/tests/generator/__fixtures__/tests_app).


## Test specific functionality that can be accessed through the `context`:

- [invoke]
        Used to run the test binary asynchronously (for details see the [binary invocation](#binary-invocation) section below).
        Returns the following tuple `(return_code: int, output: str, error: str)`.

```py
async def invoke(self, node, args = [], **kwargs)
```

- [get_test_output_parser]
        Returns a MetaBuild built-in parser (`TestReportOutParser`), the parser type should be passed as the first argument, while the second argument is a boolean that specifies if the test results should be reported by MetaBuild; the supported parsers are:
                "gtest" -> GoogleTest output parser

```py
def get_test_output_parser(self, format: str, report_results = True)
```

- [parse_report_file]
        Parses the given report file using the format specified as parameter and returns a list of `TestResult`.
        The supported report file formats are:
                "junit" -> JUnit format used by the Google Test framework.
        The `TestResult` contains the following information:

```py
def parse_report_file(self, format: str, file_path: str)
```

- [report_test_result] 
        Adds the test result to the MetaBuild test report. The first version of this function can be used with a test_result returned by
        `report_test_result` (see above), while in the second version the arguments can be specified individually.
        For more information regarding test reporting see [metabuild test]({{ site.baseurl }}{% link _docs/cli/metabuild_test.md %}).

```py
def report_test_result(self, test_result)
```

```py
def report_test_result(self, suite: str, test_case: str, success: bool, message: str = "", duration: float = 0)
```

## Binary Invocation

The `context.invoke` method accepts a specific MetaBuild node to invoke and a list of arguments that are passed to the invoked process.
It also accepts additional optional named arguments passed through `**kwargs` that can be used to access testing specific functionality.

MetaBuild provides two options to process the test results, through a callback function/functor that will parse each line of output in real time, and by
parsing the generated report file.


| Named Argument | Type | Description |
|-----------|------|-------------|
| `output_handler` | function/functor | Callable that is used to parse the unit test executable output. For unit tests using the GoogleTest framework MetaBuild has a builtin output handler that can be obtained by calling `context.get_test_output_parser("gtest")` |
| `test_invoker` | `String` | Overrides the test invoker used by MetaBuild (currently used on UWP to override the default invoker `cdb.exe` with `vstest.console` if `uwp_vstest_console` is passed as parameter) |
| `timeout` | `float` | (Optional) Number of seconds the process is allowed to run. If the process does not terminate after timeout seconds a `MetaShellException` is raised. |
| `android_destination` | `String` | (Optional) Used on android, it represents the transport id of the android virtual device to execute the binary on. MetaBuild raises a `MetaException` if it does not find the device with the given transport id in the list of active devices on the machine. |
| `xcode_destination` | `String` | (Optional) Represents the destination id of an ios device that is going to be used to execute the binary on. |


Depending on platform metabuild runs the executable through the following test invokers:

- [subprocess.Popen] - standard way of running binaries from python, this is used on xcode_macos, cmake_macos, cmake_linux, msvs_win32
- [node] - used only on cmake_wasm
- [CDB.exe] - used by default on msvs_uwp
- [vstest.console] - used on msvs_uwp if specifically requested through the `test_invoker` parameter
- [xcrun simctl] - used on xcode_ios
- [adb] - used to deploy and execute the binary on the Android emulator

For test binaries that run sandboxed (android, ios, uwp, wasm) the return value of `context.invoke` is not that of the test binary invoked.

### Binary invocation on Android

MetaBuild provides experimental support for test (binary) invocation on android. It currently supports only invocation on the android emulator from a MacOs system.
The only android sdk version supported for now is `Api level 30` (avd configuration `system-images;android-30;google_apis;x86`). Other versions may be used, given that the emulator and virtual device is setup before running metabuild and the `transport id` of the active avd is provided as a parameter to the invoker. (see the `android_destination` parameter above)
If a given transport id is not provided in the `android_destination` parameter MetaBuild will run the android emulator, create an avd (Android Virtual Device) named `metabuild_invoker_avd`, restart the `adb` server as root an run `adb push` and `adb shell` commands to deploy and execute the binary on the emulator. Unless an `android_destination` is specified on invocation multiple tests will run on the same emulator. After MetaBuild finishes running the tests it will terminate the emulator and remove the created avd. 

### Binary invocation on IOS

MetaBuild provides support for invoking test binaries on IOS. If the `xcode_destination` parameter is provided to the invoker MetaBuild will boot and use the given device, otherwise it will use one of the devices that are available on the machine. Once the destination has been determined MetaBuild will run `simctl install` and `simclt launch` to deploy and run the test binary.

### Binary invocation on UWP

By default MetaBuild uses `cbd.exe` to invoke binaries on UWP once they have been deployed. Alternatively the user can set the `test_invoker` parameter to  `uwp_vstest_console` to invoke UWP specific tests with `vstest.console`.
When invoking binaries through `cbd.exe` the value returned by `context.invoke` will not be the return value of the test application.

## Tests Filtering

By default we do not include tests from dependency projects. To allow including tests from dependency projects, use the config value [`include_dependency_tests = true`](https://git.corp.adobe.com/meta-build/meta-build/blob/0.1.556/metabuild/config/default_config.yaml#L188).

Tests filtering can be done through the cli while running `metabuild test` by using the `--labels` parameter and specifying a test `label`. Only tests that have a matching `label` in the test node will be run.

Another way to filter tests can be done at prepare stage through the `META.lock` file by using the following API:

- [test_enabled] specifies if the test is enabled/disabled through a boolean value
        Example: 
        ```
                [tests_app//test:lib1_test1]
                test_enabled = True, this test should run
        ```
- [node_tests_enabled] specifies if all the tests for a node or project are enabled/disabled through a boolean value
        Example:
        ```
                [tests_app//:lib1]
                node_tests_enabled = False, "for testing purposes"
        ```

When both `test_enabled` and `node_tests_enabled` would affect the same test the `test_enabled` option will have precedence. This way users can easily run only specific tests for a library by disabling all tests for the library (using `node_tests_enabled`) and enabling specific ones with `test_enabled`.

