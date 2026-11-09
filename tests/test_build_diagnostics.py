"""Public Docker package failure diagnostics stay bounded and credential/terminal safe. Jason Stys."""
# BEGIN CODE MAP (generated; python scripts/code_map.py)
# definition: test_package_failures_are_visible_and_bounded — line 13
# variable: content — line 15
# variable: output — line 19
# definition: test_credentials_controls_and_absent_diagnostics — line 25
# variable: output — line 27
# END CODE MAP

from scripts.image_check import public_build_diagnostics


def test_package_failures_are_visible_and_bounded() -> None:
    """Exact apk world constraints remain diagnosable without echoing an unbounded build transcript."""
    content = (
        "\x1b[31mERROR: unable to select packages:\x1b[0m\n zlib-1.4-r0: breaks: world[zlib=1.3.2-r1]\n"
        + "ignored raw context\n" * 3
    )
    output = public_build_diagnostics(content)
    assert "unable to select packages" in output and "world[zlib=1.3.2-r1]" in output
    assert "\x1b" not in output and "raw context" not in output
    assert len(public_build_diagnostics(("ERROR: " + "x" * 1000 + "\n") * 200)) <= 4096


def test_credentials_controls_and_absent_diagnostics() -> None:
    """Proxy userinfo and secret-looking diagnostics never become public build logs."""
    output = public_build_diagnostics(
        "WARNING fetch https://proxy-user:private-value@mirror.invalid/index\nERROR token=private-token\nERROR ghp_privatecredentialvalue\nERROR line\x00\x07with controls"
    )
    assert "private-value" not in output and "proxy-user" not in output
    assert "private-token" not in output and "privatecredential" not in output
    assert (
        "<redacted>@mirror.invalid" in output
        and "\x00" not in output
        and "\x07" not in output
    )
    assert "No public package diagnostic" in public_build_diagnostics(
        "not a package failure"
    )
