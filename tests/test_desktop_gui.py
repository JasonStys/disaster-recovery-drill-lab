"""Presentation-adapter unit tests with real core/SQLite workers; real widgets are separately frozen-tested. Jason Stys."""
# BEGIN CODE MAP (generated; python scripts/code_map.py)
# definition: Variable — line 220
# definition: __init__ — line 223
# parameter: self — line 223
# parameter: value — line 223
# definition: get — line 227
# parameter: self — line 227
# definition: set — line 231
# parameter: self — line 231
# parameter: value — line 231
# variable: callback — line 234
# definition: trace_add — line 237
# parameter: _event — line 237
# parameter: callback — line 237
# parameter: self — line 237
# definition: Widget — line 242
# definition: __init__ — line 245
# parameter: _args — line 245
# parameter: kwargs — line 245
# parameter: self — line 245
# parameter: _items — line 249
# definition: pack — line 251
# parameter: _kwargs — line 251
# parameter: self — line 251
# definition: grid — line 254
# parameter: _kwargs — line 254
# parameter: self — line 254
# definition: grid_remove — line 257
# parameter: self — line 257
# definition: columnconfigure — line 260
# parameter: _args — line 260
# parameter: _kwargs — line 260
# parameter: self — line 260
# definition: add — line 263
# parameter: _args — line 263
# parameter: _kwargs — line 263
# parameter: self — line 263
# definition: theme_use — line 266
# parameter: _args — line 266
# parameter: self — line 266
# definition: configure — line 269
# parameter: _args — line 269
# parameter: kwargs — line 269
# parameter: self — line 269
# definition: heading — line 273
# parameter: _args — line 273
# parameter: _kwargs — line 273
# parameter: self — line 273
# definition: column — line 276
# parameter: _args — line 276
# parameter: _kwargs — line 276
# parameter: self — line 276
# definition: bind — line 279
# parameter: _args — line 279
# parameter: self — line 279
# definition: yview — line 282
# parameter: _args — line 282
# parameter: self — line 282
# definition: set — line 285
# parameter: _args — line 285
# parameter: self — line 285
# definition: state — line 288
# parameter: flags — line 288
# parameter: self — line 288
# variable: flag — line 290
# definition: invoke — line 296
# parameter: self — line 296
# definition: insert — line 302
# parameter: _parent — line 302
# parameter: _position — line 302
# parameter: iid — line 302
# parameter: self — line 302
# parameter: values — line 302
# definition: delete — line 306
# parameter: items — line 306
# parameter: self — line 306
# variable: item — line 308
# variable: item — line 310
# definition: get_children — line 312
# parameter: self — line 312
# definition: selection — line 316
# parameter: self — line 316
# definition: selection_set — line 320
# parameter: identity — line 320
# parameter: self — line 320
# definition: Text — line 326
# definition: delete — line 329
# parameter: _args — line 329
# parameter: self — line 329
# definition: insert — line 333
# parameter: _position — line 333
# parameter: self — line 333
# parameter: text — line 333
# definition: Root — line 338
# definition: __init__ — line 341
# parameter: self — line 341
# definition: title — line 346
# parameter: _args — line 346
# parameter: self — line 346
# definition: geometry — line 349
# parameter: _args — line 349
# parameter: self — line 349
# definition: minsize — line 352
# parameter: _args — line 352
# parameter: self — line 352
# definition: protocol — line 355
# parameter: _event — line 355
# parameter: callback — line 355
# parameter: self — line 355
# definition: after — line 359
# parameter: _delay — line 359
# parameter: callback — line 359
# parameter: self — line 359
# definition: destroy — line 363
# parameter: self — line 363
# definition: mainloop — line 367
# parameter: self — line 367
# variable: _ — line 371
# definition: presentation — line 379
# parameter: monkeypatch — line 379
# parameter: _parent — line 384
# variable: name — line 386
# variable: messages — line 400
# parameter: _kwargs — line 402
# parameter: args — line 402
# parameter: _kwargs — line 405
# parameter: args — line 405
# definition: app — line 411
# parameter: presentation — line 411
# parameter: tmp_path — line 411
# variable: state — line 413
# variable: root — line 414
# variable: window — line 415
# definition: settle — line 429
# parameter: window — line 429
# variable: deadline — line 431
# definition: test_real_controller_run_filter_detail_history_export_and_help — line 438
# parameter: app — line 439
# parameter: monkeypatch — line 439
# parameter: presentation — line 439
# parameter: tmp_path — line 439
# parameter: _kwargs — line 465
# variable: original — line 467
# variable: exported — line 469
# variable: path — line 470
# parameter: _kwargs — line 475
# definition: test_explicit_retention_confirmation_removes_only_selected_local_copy — line 481
# parameter: app — line 482
# parameter: monkeypatch — line 482
# parameter: tmp_path — line 482
# variable: exported — line 492
# variable: original — line 493
# parameter: _args — line 494
# parameter: _kwargs — line 494
# parameter: _args — line 497
# parameter: _kwargs — line 497
# variable: path — line 500
# definition: test_input_selection_cancel_busy_failure_and_literal_row_cap — line 507
# parameter: app — line 508
# parameter: monkeypatch — line 508
# parameter: tmp_path — line 508
# variable: name — line 511
# parameter: _kwargs — line 515
# parameter: _kwargs — line 520
# parameter: _kwargs — line 523
# variable: kind — line 525
# variable: value — line 529
# parameter: _kwargs — line 530
# variable: index — line 555
# definition: test_close_retains_lock_until_actual_core_transaction_finishes — line 569
# parameter: app — line 570
# parameter: monkeypatch — line 570
# parameter: tmp_path — line 570
# variable: ready — line 573
# variable: release — line 573
# variable: actual — line 574
# definition: pause — line 576
# parameter: args — line 576
# variable: reopened — line 594
# definition: test_main_native_close_and_rejected_acceptance_paths — line 601
# parameter: monkeypatch — line 602
# parameter: presentation — line 602
# parameter: tmp_path — line 602
# variable: actual — line 605
# definition: create — line 607
# parameter: root — line 607
# parameter: state — line 607
# variable: window — line 609
# variable: profile — line 614
# variable: reopened — line 616
# variable: unknown — line 640
# definition: test_switching_mode_ignores_hidden_catalog_controls_and_prior_row — line 648
# parameter: app — line 649
# parameter: monkeypatch — line 649
# parameter: tmp_path — line 649
# variable: source — line 652
# variable: original — line 653
# variable: captured — line 662
# variable: save — line 663
# definition: record — line 665
# parameter: files — line 665
# parameter: kind — line 665
# parameter: parameters — line 665
# parameter: summary — line 665
# END CODE MAP

import threading
import time
from types import SimpleNamespace

import pytest

from dr import desktop as module
from dr import desktop_project as project
from dr.desktop_io import Rejected
from dr.desktop_state import Workspace


class Variable:
    """Inert presentation variable; invokes the same registered GUI trace callbacks."""

    def __init__(self, value=""):
        """Keep a scalar control value and registered change callbacks."""
        self.value, self.callbacks = value, []

    def get(self):
        """Return the current presentation control value."""
        return self.value

    def set(self, value):
        """Change a control and exercise actual application rendering callbacks."""
        self.value = value
        for callback in self.callbacks:
            callback()

    def trace_add(self, _event, callback):
        """Retain the GUI's value-change handler."""
        self.callbacks.append(callback)


class Widget:
    """Minimal inert ttk presentation adapter; no core, storage or analysis output is mocked."""

    def __init__(self, *_args, **kwargs):
        """Retain properties, rows and command closures."""
        self.options, self.rows, self.selected = kwargs, {}, ()
        self.flags = set()
        self.tk = SimpleNamespace(call=lambda *_items: None)

    def pack(self, **_kwargs):
        """Accept presentation layout."""

    def grid(self, **_kwargs):
        """Accept presentation grid coordinates."""

    def grid_remove(self):
        """Accept operation-specific hidden controls."""

    def columnconfigure(self, *_args, **_kwargs):
        """Accept resize weights."""

    def add(self, *_args, **_kwargs):
        """Accept notebook/paned-window children."""

    def theme_use(self, *_args):
        """Accept native style selection."""

    def configure(self, *_args, **kwargs):
        """Retain updated widget options."""
        self.options.update(kwargs)

    def heading(self, *_args, **_kwargs):
        """Accept a literal table heading."""

    def column(self, *_args, **_kwargs):
        """Accept table sizing."""

    def bind(self, *_args):
        """Accept event registration; tests invoke actual handlers explicitly."""

    def yview(self, *_args):
        """Accept scroll requests."""

    def set(self, *_args):
        """Accept scrollbar position updates."""

    def state(self, flags):
        """Preserve disabled controls so a simulated click cannot bypass a busy guard."""
        for flag in flags:
            if flag.startswith("!"):
                self.flags.discard(flag[1:])
            else:
                self.flags.add(flag)

    def invoke(self):
        """Invoke the actual registered command unless the control is disabled."""
        if "disabled" not in self.flags:
            return self.options["command"]()
        return None

    def insert(self, _parent, _position, *, iid, values):
        """Retain exact rows inserted by real project rendering."""
        self.rows[iid] = values

    def delete(self, *items):
        """Remove rows and their selections like a real treeview."""
        for item in items:
            self.rows.pop(item, None)
        self.selected = tuple(item for item in self.selected if item in self.rows)

    def get_children(self):
        """Return displayed row identities."""
        return tuple(self.rows)

    def selection(self):
        """Return the current selected row identity."""
        return self.selected

    def selection_set(self, identity):
        """Select one existing row like a real single-selection control."""
        assert identity in self.rows
        self.selected = (identity,)


class Text(Widget):
    """Retain literal detail output without interpreting markup or executing event fields."""

    def delete(self, *_args):
        """Clear existing literal detail text."""
        self.text = ""

    def insert(self, _position, text):
        """Retain the exact rendered detail text."""
        self.text = text


class Root:
    """Deterministic presentation event queue; actual Tk mainloops are independently exercised by frozen acceptance."""

    def __init__(self):
        """Create a fresh owned presentation root."""
        self.callbacks, self.destroyed = [], False
        self.on_loop = None

    def title(self, *_args):
        """Accept window title."""

    def geometry(self, *_args):
        """Accept initial geometry."""

    def minsize(self, *_args):
        """Accept minimum geometry."""

    def protocol(self, _event, callback):
        """Keep the application's native close callback."""
        self.close_callback = callback

    def after(self, _delay, callback):
        """Queue the actual lifecycle callback without a platform display server."""
        self.callbacks.append(callback)

    def destroy(self):
        """Mark only this owned root as closed."""
        self.destroyed = True

    def mainloop(self):
        """Run the requested test lifecycle using real application callbacks."""
        if self.on_loop:
            self.on_loop()
        for _ in range(200):
            if self.destroyed:
                return
            self.callbacks.pop(0)()
        raise AssertionError("presentation lifecycle did not close")


@pytest.fixture
def presentation(monkeypatch):
    """Replace only OS presentation surfaces; real worker, core, SQLite and export code remain active."""
    monkeypatch.setattr(module.tk, "StringVar", Variable)
    monkeypatch.setattr(module.tk, "BooleanVar", Variable)
    monkeypatch.setattr(module.tk, "Tk", Root)
    monkeypatch.setattr(module.tk, "Toplevel", lambda _parent: Root())
    monkeypatch.setattr(module.tk, "Text", Text)
    for name in (
        "Frame",
        "Label",
        "Notebook",
        "Combobox",
        "Entry",
        "Button",
        "Checkbutton",
        "Panedwindow",
        "Treeview",
        "Scrollbar",
        "Style",
    ):
        monkeypatch.setattr(module.ttk, name, Widget)
    messages = []
    monkeypatch.setattr(
        module.messagebox, "showinfo", lambda *args, **_kwargs: messages.append(args)
    )
    monkeypatch.setattr(
        module.messagebox, "showerror", lambda *args, **_kwargs: messages.append(args)
    )
    return messages


@pytest.fixture
def app(tmp_path, presentation):
    """Build the actual workbench controller against an isolated real durable workspace."""
    state = Workspace(tmp_path / "profile", project.PRODUCT, project.ROOT)
    root = Root()
    window = module.Workbench(root, state)
    # Presentation tests exercise the real offline domain engine and SQLite;
    # actual widgets/mainloop are separately proved by the final frozen consumer.
    window.prepared.set(project.SCENARIOS[1])
    window.load_prepared()
    try:
        yield window
    finally:
        if window.worker_thread:
            window.worker_thread.join(10)
            assert not window.worker_thread.is_alive()
        state.close()


def settle(window):
    """Observe completion of one actual owned analysis; no retries or invented report values."""
    deadline = time.monotonic() + 10
    while window.busy and time.monotonic() < deadline:
        window.poll()
        time.sleep(0.005)
    assert not window.busy


def test_real_controller_run_filter_detail_history_export_and_help(
    app, tmp_path, monkeypatch, presentation
):
    """Real core results drive controls, literal filters, exact private exports and history reopening."""
    app.export()
    assert "completed" in app.status.get()
    app.run_button.invoke()
    assert not app.busy and app.state.history() == []
    app.authorized.set(True)
    app.run_button.invoke()
    settle(app)
    assert app.selected_run == 1 and len(app.state.history()) == 1
    assert len(app.table.get_children()) > 0
    app.table.selection_set("0")
    app.inspect()
    assert "{" in app.details.text
    app.review_selected()
    if project.REVIEW_MODE is not None:
        assert app.mode.get() == project.REVIEW_MODE and app.authorized.get() is False
    app.search.set("not-a-supported-record-never-present")
    assert app.table.get_children() == ()
    app.inspect()
    app.search.set("")
    app.history_table.selection_set("1")
    app.open_button.invoke()
    assert "without re-running" in app.status.get()
    monkeypatch.setattr(
        module.filedialog, "askdirectory", lambda **_kwargs: str(tmp_path)
    )
    original = app.state.files(1)
    app.export_button.invoke()
    exported = next(tmp_path.glob(project.PRODUCT + "-run-*"))
    assert {path.name: path.read_bytes() for path in exported.iterdir()} == original
    app.help()
    assert "plaintext" in presentation[-1][1]
    app.licenses()
    monkeypatch.setattr(
        module.filedialog, "askdirectory", lambda **_kwargs: str(tmp_path / "missing")
    )
    app.export()
    assert "unavailable" in app.status.get()


def test_explicit_retention_confirmation_removes_only_selected_local_copy(
    app, tmp_path, monkeypatch
):
    """Cancellation preserves data; confirmation deletes one exact DB bundle without touching a prior export."""
    app.remove_history()
    assert "Select" in app.status.get()
    app.review_selected()
    app.authorized.set(True)
    app.run_button.invoke()
    settle(app)
    app.history_table.selection_set("1")
    exported = app.state.export(1, tmp_path, project.PRODUCT)
    original = app.state.files(1)
    monkeypatch.setattr(module.messagebox, "askyesno", lambda *_args, **_kwargs: False)
    app.remove_button.invoke()
    assert app.state.files(1) == original
    monkeypatch.setattr(module.messagebox, "askyesno", lambda *_args, **_kwargs: True)
    app.remove_button.invoke()
    assert app.state.history() == [] and app.selected_run == 0
    assert {path.name: path.read_bytes() for path in exported.iterdir()} == original
    app.busy = True
    app.remove_history()
    assert "Wait" in app.status.get()
    app.busy = False


def test_input_selection_cancel_busy_failure_and_literal_row_cap(
    app, tmp_path, monkeypatch
):
    """Operator mistakes do not silently run a prepared fixture, overwrite results or defeat close semantics."""
    name = "document"
    monkeypatch.setattr(
        module.filedialog,
        "askopenfilename",
        lambda **_kwargs: str(tmp_path / "authorized.json"),
    )
    monkeypatch.setattr(
        module.filedialog,
        "askopenfilenames",
        lambda **_kwargs: ("one.json", "two.json"),
    )
    monkeypatch.setattr(
        module.filedialog, "askdirectory", lambda **_kwargs: str(tmp_path)
    )
    for kind in ("file", "files", "directory"):
        app.authorized.set(True)
        app.choose(name, kind)
        assert app.authorized.get() is False
    value = app.values[name].get()
    monkeypatch.setattr(module.filedialog, "askopenfilename", lambda **_kwargs: "")
    app.choose(name, "file")
    assert app.values[name].get() == value
    app.busy = True
    app.choose(name, "file")
    app.load_prepared()
    app.open_history()
    app.run()
    assert app.state.history() == []
    app.busy = False
    app.load_prepared()
    app.mode.set("unsupported-operation")
    app.authorized.set(True)
    app.run()
    settle(app)
    assert "rejected" in app.status.get().lower() and app.state.history() == []
    app.current = {
        "bounded": [
            {
                "kind": "objective",
                "name": str(index),
                "observed": 1,
                "budget": 2,
                "met": True,
            }
            for index in range(5001)
        ]
    }
    app.view.set("bounded")
    app.render()
    assert len(app.table.get_children()) == 5000
    app.search.set('"5000"')
    assert len(app.table.get_children()) == 1
    app.exit()
    app.run()
    app.poll()
    assert app.root.destroyed and app.state.lock == -1


def test_close_retains_lock_until_actual_core_transaction_finishes(
    app, tmp_path, monkeypatch
):
    """An in-flight real analysis is drained rather than abandoned, force-killed or exposed to a second owner."""
    ready, release = threading.Event(), threading.Event()
    actual = project.analyze

    def pause(*args):
        """Control only scheduling; completion still invokes the actual project core and durable output."""
        ready.set()
        assert release.wait(5)
        return actual(*args)

    monkeypatch.setattr(project, "analyze", pause)
    app.authorized.set(True)
    app.run_button.invoke()
    assert ready.wait(3)
    app.exit()
    app.poll()
    assert not app.root.destroyed and app.busy
    with pytest.raises((Rejected, OSError)):
        Workspace(app.state.path, project.PRODUCT, project.ROOT)
    release.set()
    settle(app)
    assert app.root.destroyed and app.state.lock == -1
    reopened = Workspace(app.state.path, project.PRODUCT, project.ROOT)
    try:
        assert len(reopened.history()) == 1
    finally:
        reopened.close()


def test_main_native_close_and_rejected_acceptance_paths(
    tmp_path, presentation, monkeypatch
):
    """Normal startup never auto-analyzes; test flags cannot enter existing real-profile state or claim partial success."""
    actual = module.Workbench

    def create(root, state):
        """Use actual controls/controller; request the normal close callback at the start of the event loop."""
        window = actual(root, state)
        root.on_loop = window.exit
        return window

    monkeypatch.setattr(module, "Workbench", create)
    profile = tmp_path / "normal"
    assert module.main(["--profile", str(profile)]) == 0
    reopened = Workspace(profile, project.PRODUCT, project.ROOT)
    assert reopened.history() == []
    reopened.close()
    with pytest.raises(SystemExit):
        module.main(["--acceptance-output", str(tmp_path / "output")])
    with pytest.raises(SystemExit):
        module.main(["--acceptance-reopen"])
    assert (
        module.main(
            ["--profile", str(profile), "--acceptance-output", str(tmp_path / "output")]
        )
        == 2
    )
    assert (
        module.main(
            [
                "--profile",
                str(tmp_path / "synthetic"),
                "--acceptance-output",
                str(tmp_path / "new-output"),
            ]
        )
        == 2
    )
    unknown = tmp_path / "unknown"
    unknown.mkdir()
    (unknown / "keep").write_bytes(b"unchanged")
    assert module.main(["--profile", str(unknown)]) == 2
    assert (unknown / "keep").read_bytes() == b"unchanged"
    assert presentation and "No saved evidence was reset" in presentation[-1][1]


def test_switching_mode_ignores_hidden_catalog_controls_and_prior_row(
    app, tmp_path, monkeypatch
):
    """The real evaluation neither applies inactive catalog overrides nor persists old selected evidence."""
    source = tmp_path / "evaluation.json"
    original = (project.ROOT / "examples/objective-evaluation.json").read_bytes()
    source.write_bytes(original)
    app.mode.set(project.MODES[0])
    app.values["document"].set(str(source))
    app.values["as_of_ms"].set("invalid hidden catalog clock")
    app.values["retention_minimum"].set("20")
    app.visible = [{"prior_selected_record": "not current input"}]
    app.table.insert("", "end", iid="0", values=("old",))
    app.table.selection_set("0")
    captured = []
    save = app.state.save

    def record(kind, summary, parameters, files):
        """Observe actual committed parameters without replacing the domain engine or durable save."""
        captured.append(dict(parameters))
        return save(kind, summary, parameters, files)

    monkeypatch.setattr(app.state, "save", record)
    app.authorized.set(True)
    app.run_button.invoke()
    settle(app)
    assert app.selected_run == 1
    assert captured == [
        {
            "mode": project.MODES[0],
            "document": str(source),
            "rto_ms": "",
            "rpo_ms": "",
            "max_lost_orders": "",
        }
    ]
    assert source.read_bytes() == original
    assert b'"snapshot_matches":true' in app.state.files(1)["restore-evaluation.json"]
