import sys
import csv
from datetime import date
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont


if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).parent

FILE_PATH = BASE_DIR / "output_progress.csv"


DEV_POINTS = {
    "QM Warranty": 0.75,
    "PM": 0.25,
    "Minor Repair": 0.50,
    "Flat Rate": 1.0,
    "Manufacture Warranty": 1.0,
}

STRATUS_POINTS = 0.75
HOMEFILL_POINTS = 2.0


def load_progress():
    if FILE_PATH.exists():
        try:
            with FILE_PATH.open(newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    state = {
                        "output": int(row.get("output", 0)),
                        "weighted_output": float(row.get("weighted_output", 0.0)),
                        "count_stratus": int(row.get("count_stratus", 0)),
                        "count_stratus_flat": int(row.get("count_stratus_flat", 0)),
                        "count_stratus_manuf": int(row.get("count_stratus_manuf", 0)),
                        "count_homefill": int(row.get("count_homefill", 0)),
                        "count_homefill_flat": int(row.get("count_homefill_flat", 0)),
                        "count_homefill_manuf": int(row.get("count_homefill_manuf", 0)),
                        "count_qm": int(row.get("count_qm", 0)),
                        "count_pm": int(row.get("count_pm", 0)),
                        "count_minor": int(row.get("count_minor", 0)),
                        "count_flat": int(row.get("count_flat", 0)),
                        "count_manuf": int(row.get("count_manuf", 0)),
                        "count_1025_qm": int(row.get("count_1025_qm", 0)),
                        "count_1025_pm": int(row.get("count_1025_pm", 0)),
                        "count_1025_minor": int(row.get("count_1025_minor", 0)),
                        "count_1025_flat": int(row.get("count_1025_flat", 0)),
                        "count_1025_manuf": int(row.get("count_1025_manuf", 0)),
                        "start_date": row.get("start_date") or "",
                        "start_of_day_output": int(row.get("start_of_day_output", 0)),
                    }
                    # migrate/sync Stratus totals vs subcategories
                    sub = state.get("count_stratus_flat", 0) + state.get("count_stratus_manuf", 0)
                    if sub > 0:
                        state["count_stratus"] = sub
                    elif state.get("count_stratus", 0) > 0 and sub == 0:
                        state["count_stratus_flat"] = state.get("count_stratus", 0)
                        state["count_stratus_manuf"] = 0
                    # ensure start-of-day values
                    today = date.today().isoformat()
                    if state.get("start_date") != today:
                        state["start_date"] = today
                        state["start_of_day_output"] = state.get("output", 0)
                        # write back immediately so other processes see it
                        save_progress(state)
                    return state
        except Exception:
            pass
    return {
        "output": 0,
        "weighted_output": 0.0,
        "count_stratus": 0,
        "count_stratus_flat": 0,
        "count_stratus_manuf": 0,
        "count_homefill": 0,
        "count_homefill_flat": 0,
        "count_homefill_manuf": 0,
        "count_qm": 0,
        "count_pm": 0,
        "count_minor": 0,
        "count_flat": 0,
        "count_manuf": 0,
        "count_1025_qm": 0,
        "count_1025_pm": 0,
        "count_1025_minor": 0,
        "count_1025_flat": 0,
        "count_1025_manuf": 0,
        "start_date": date.today().isoformat(),
        "start_of_day_output": 0,
    }


def save_progress(state):
    with FILE_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "output",
                "weighted_output",
                "count_stratus",
                "count_stratus_flat",
                "count_stratus_manuf",
                "count_homefill",
                "count_homefill_flat",
                "count_homefill_manuf",
                "count_qm",
                "count_pm",
                "count_minor",
                "count_flat",
                "count_manuf",
                "count_1025_qm",
                "count_1025_pm",
                "count_1025_minor",
                "count_1025_flat",
                "count_1025_manuf",
                "start_date",
                "start_of_day_output",
            ],
        )
        writer.writeheader()
        writer.writerow(
            {
                "output": state["output"],
                "weighted_output": state["weighted_output"],
                "count_stratus": state.get("count_stratus", 0),
                "count_stratus_flat": state.get("count_stratus_flat", 0),
                "count_stratus_manuf": state.get("count_stratus_manuf", 0),
                "count_homefill": state.get("count_homefill", 0),
                "count_homefill_flat": state.get("count_homefill_flat", 0),
                "count_homefill_manuf": state.get("count_homefill_manuf", 0),
                "count_qm": state.get("count_qm", 0),
                "count_pm": state.get("count_pm", 0),
                "count_minor": state.get("count_minor", 0),
                "count_flat": state.get("count_flat", 0),
                "count_manuf": state.get("count_manuf", 0),
                "count_1025_qm": state.get("count_1025_qm", 0),
                "count_1025_pm": state.get("count_1025_pm", 0),
                "count_1025_minor": state.get("count_1025_minor", 0),
                "count_1025_flat": state.get("count_1025_flat", 0),
                "count_1025_manuf": state.get("count_1025_manuf", 0),
                "start_date": state.get("start_date", date.today().isoformat()),
                "start_of_day_output": state.get("start_of_day_output", 0),
            }
        )


class WeightedOutputApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Weighted Output Tracker")
        # Bold font for totals in breakdown
        try:
            self.bold_font = tkfont.nametofont("TkDefaultFont").copy()
            self.bold_font.configure(weight="bold")
        except Exception:
            self.bold_font = (None, 10, "bold")
        self.state = load_progress()
        # ensure keys exist for older CSVs
        for k in ("count_stratus","count_homefill","count_homefill_flat","count_homefill_manuf",
                "count_qm","count_pm","count_minor","count_flat","count_manuf",
                "count_1025_qm","count_1025_pm","count_1025_minor","count_1025_flat","count_1025_manuf"):
            self.state.setdefault(k, 0)
        # ensure start-of-day on startup
        self._ensure_start_of_day()

        self._build_ui()
        self._refresh_totals()

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_ui(self):
        container = ttk.Frame(self, padding=12)
        container.grid(row=0, column=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Totals row
        totals = ttk.Frame(container)
        totals.grid(row=0, column=0, sticky="ew")
        totals.columnconfigure(1, weight=1)
        totals.columnconfigure(3, weight=1)
        totals.columnconfigure(6, weight=1)
        totals.columnconfigure(9, weight=1)

        ttk.Label(totals, text="Total Output:").grid(row=0, column=0, sticky="w")
        self.output_var = tk.StringVar()
        ttk.Label(totals, textvariable=self.output_var).grid(row=0, column=1, sticky="w")

        # Started today with (editable) next to Total Output
        ttk.Label(totals, text="Started today with:").grid(row=0, column=2, sticky="e", padx=(24, 0))
        self.start_var = tk.StringVar()
        ttk.Label(totals, textvariable=self.start_var).grid(row=0, column=3, sticky="w")
        ttk.Button(totals, text="Edit", command=self._edit_start_of_day).grid(row=0, column=4, sticky="w", padx=(6,0))

        # Today's Output further right
        ttk.Label(totals, text="Today's Output:").grid(row=0, column=5, sticky="e", padx=(24, 0))
        self.today_var = tk.StringVar()
        ttk.Label(totals, textvariable=self.today_var).grid(row=0, column=6, sticky="w")
        ttk.Button(totals, text="Edit", command=self._edit_today_output).grid(row=0, column=7, sticky="w", padx=(6,0))

        ttk.Label(totals, text="Weighted Output:").grid(row=0, column=8, sticky="e", padx=(24, 0))
        self.weighted_var = tk.StringVar()
        ttk.Label(totals, textvariable=self.weighted_var).grid(row=0, column=9, sticky="w")

        ttk.Separator(container, orient="horizontal").grid(row=1, column=0, sticky="ew", pady=8)

        notebook = ttk.Notebook(container)
        notebook.grid(row=2, column=0, sticky="nsew")
        container.rowconfigure(2, weight=1)

        add_tab = ttk.Frame(notebook, padding=12)
        rem_tab = ttk.Frame(notebook, padding=12)
        brk_tab = ttk.Frame(notebook, padding=12)
        notebook.add(add_tab, text="Add")
        notebook.add(rem_tab, text="Remove")
        notebook.add(brk_tab, text="Breakdown")

        # Add Tab
        self._build_add_tab(add_tab)
        # Remove Tab
        self._build_remove_tab(rem_tab)
        # Breakdown Tab
        self._build_breakdown_tab(brk_tab)
        ttk.Button(brk_tab, text="Edit breakdown", command=self._open_edit_breakdown).grid(row=1, column=0, pady=(12,0), sticky="w")

    def _build_add_tab(self, parent):
        # Stratus add (subcategories)
        str_frame = ttk.LabelFrame(parent, text="Stratus (enter per-type quantities)", padding=8)
        str_frame.grid(row=0, column=0, sticky="ew")
        self.add_s_flat = tk.StringVar(value="0")
        self.add_s_manuf = tk.StringVar(value="0")
        self._row_inputs(str_frame, 0, [
            ("Stratus Flat Rate", self.add_s_flat),
            ("Stratus Manufacture Warranty", self.add_s_manuf),
        ])
        ttk.Button(str_frame, text="Add", command=self._add_stratus).grid(row=2, column=0, pady=(6, 0), sticky="w")

        # Homefill add (subcategories)
        hf_frame = ttk.LabelFrame(parent, text="Homefill (enter per-type quantities)", padding=8)
        hf_frame.grid(row=1, column=0, sticky="ew", pady=(10, 0))
        self.add_h_flat = tk.StringVar(value="0")
        self.add_h_manuf = tk.StringVar(value="0")
        self._row_inputs(hf_frame, 0, [
            ("Homefill Flat Rate", self.add_h_flat),
            ("Homefill Manufacture Warranty", self.add_h_manuf),
        ])
        ttk.Button(hf_frame, text="Add", command=self._add_homefill).grid(row=2, column=0, pady=(6, 0), sticky="w")

        # 525 add
        dev = ttk.LabelFrame(parent, text="525 (enter per-warranty quantities)", padding=8)
        dev.grid(row=2, column=0, sticky="ew", pady=(10, 0))

        self.add_q = tk.StringVar(value="0")
        self.add_p = tk.StringVar(value="0")
        self.add_m = tk.StringVar(value="0")
        self.add_f = tk.StringVar(value="0")
        self.add_w = tk.StringVar(value="0")

        self._row_inputs(dev, 0, [
            ("QM Warranty", self.add_q),
            ("PM", self.add_p),
            ("Minor Repair", self.add_m),
            ("Flat Rate", self.add_f),
            ("Manufacture Warranty", self.add_w),
        ])

        ttk.Button(dev, text="Add", command=self._add_525).grid(row=2, column=0, pady=(6, 0), sticky="w")

        # 1025 add
        dev10 = ttk.LabelFrame(parent, text="1025 (enter per-warranty quantities)", padding=8)
        dev10.grid(row=3, column=0, sticky="ew", pady=(10, 0))

        self.add10_q = tk.StringVar(value="0")
        self.add10_p = tk.StringVar(value="0")
        self.add10_m = tk.StringVar(value="0")
        self.add10_f = tk.StringVar(value="0")
        self.add10_w = tk.StringVar(value="0")

        self._row_inputs(dev10, 0, [
            ("QM Warranty", self.add10_q),
            ("PM", self.add10_p),
            ("Minor Repair", self.add10_m),
            ("Flat Rate", self.add10_f),
            ("Manufacture Warranty", self.add10_w),
        ])

        ttk.Button(dev10, text="Add", command=self._add_1025).grid(row=2, column=0, pady=(6, 0), sticky="w")

    def _build_remove_tab(self, parent):
        # Stratus remove (subcategories)
        str_frame = ttk.LabelFrame(parent, text="Stratus (enter per-type quantities)", padding=8)
        str_frame.grid(row=0, column=0, sticky="ew")
        self.rem_s_flat = tk.StringVar(value="0")
        self.rem_s_manuf = tk.StringVar(value="0")
        self._row_inputs(str_frame, 0, [
            ("Stratus Flat Rate", self.rem_s_flat),
            ("Stratus Manufacture Warranty", self.rem_s_manuf),
        ])
        ttk.Button(str_frame, text="Remove", command=self._remove_stratus).grid(row=2, column=0, pady=(6, 0), sticky="w")

        # Homefill remove (subcategories)
        hf_frame = ttk.LabelFrame(parent, text="Homefill (enter per-type quantities)", padding=8)
        hf_frame.grid(row=1, column=0, sticky="ew", pady=(10, 0))
        self.rem_h_flat = tk.StringVar(value="0")
        self.rem_h_manuf = tk.StringVar(value="0")
        self._row_inputs(hf_frame, 0, [
            ("Homefill Flat Rate", self.rem_h_flat),
            ("Homefill Manufacture Warranty", self.rem_h_manuf),
        ])
        ttk.Button(hf_frame, text="Remove", command=self._remove_homefill).grid(row=2, column=0, pady=(6, 0), sticky="w")

        # 525 remove
        dev = ttk.LabelFrame(parent, text="525 (enter per-warranty quantities)", padding=8)
        dev.grid(row=2, column=0, sticky="ew", pady=(10, 0))

        self.rem_q = tk.StringVar(value="0")
        self.rem_p = tk.StringVar(value="0")
        self.rem_m = tk.StringVar(value="0")
        self.rem_f = tk.StringVar(value="0")
        self.rem_w = tk.StringVar(value="0")

        self._row_inputs(dev, 0, [
            ("QM Warranty", self.rem_q),
            ("PM", self.rem_p),
            ("Minor Repair", self.rem_m),
            ("Flat Rate", self.rem_f),
            ("Manufacture Warranty", self.rem_w),
        ])

        ttk.Button(dev, text="Remove", command=self._remove_525).grid(row=2, column=0, pady=(6, 0), sticky="w")

        # 1025 remove
        dev10 = ttk.LabelFrame(parent, text="1025 (enter per-warranty quantities)", padding=8)
        dev10.grid(row=3, column=0, sticky="ew", pady=(10, 0))

        self.rem10_q = tk.StringVar(value="0")
        self.rem10_p = tk.StringVar(value="0")
        self.rem10_m = tk.StringVar(value="0")
        self.rem10_f = tk.StringVar(value="0")
        self.rem10_w = tk.StringVar(value="0")

        self._row_inputs(dev10, 0, [
            ("QM Warranty", self.rem10_q),
            ("PM", self.rem10_p),
            ("Minor Repair", self.rem10_m),
            ("Flat Rate", self.rem10_f),
            ("Manufacture Warranty", self.rem10_w),
        ])

        ttk.Button(dev10, text="Remove", command=self._remove_1025).grid(row=2, column=0, pady=(6, 0), sticky="w")

    def _row_inputs(self, parent, start_row, pairs):
        # Helper to place label/entry pairs in grid, two per row if space
        col = 0
        row = start_row
        for label, var in pairs:
            ttk.Label(parent, text=label+":").grid(row=row, column=col, sticky="w", pady=2)
            ttk.Entry(parent, textvariable=var, width=8).grid(row=row, column=col+1, padx=(6, 18))
            col += 2
            if col >= 6:
                col = 0
                row += 1

    def _refresh_totals(self):
        # rollover start-of-day if the date changed
        self._ensure_start_of_day()
        self.output_var.set(str(self.state["output"]))
        self.weighted_var.set(f"{self.state['weighted_output']:.2f}")
        self.start_var.set(str(self.state.get("start_of_day_output", 0)))
        # compute today's output as total minus start-of-day
        today = max(0, self.state.get("output", 0) - self.state.get("start_of_day_output", 0))
        self.today_var.set(str(today))
        # refresh breakdown labels if present
        if hasattr(self, "bd_labels"):
            self._refresh_breakdown()

    def _ensure_start_of_day(self):
        today = date.today().isoformat()
        if self.state.get("start_date") != today:
            self.state["start_date"] = today
            self.state["start_of_day_output"] = self.state.get("output", 0)
            save_progress(self.state)

    # ---- Add handlers ----
    def _add_stratus(self):
        s_flat = self._parse_nonneg(self.add_s_flat)
        s_manuf = self._parse_nonneg(self.add_s_manuf)
        qty = s_flat + s_manuf
        if qty == 0:
            messagebox.showinfo("No Action", "Enter at least one Stratus quantity to add.")
            return
        self.state["output"] += qty
        self.state["weighted_output"] += STRATUS_POINTS * qty
        self.state["count_stratus_flat"] = self.state.get("count_stratus_flat", 0) + s_flat
        self.state["count_stratus_manuf"] = self.state.get("count_stratus_manuf", 0) + s_manuf
        self.state["count_stratus"] = self.state.get("count_stratus", 0) + qty
        save_progress(self.state)
        self._refresh_totals()
        messagebox.showinfo("Added", f"Added {qty} Stratus unit(s).")

    def _add_homefill(self):
        h_flat = self._parse_nonneg(self.add_h_flat)
        h_manuf = self._parse_nonneg(self.add_h_manuf)
        qty = h_flat + h_manuf
        if qty == 0:
            messagebox.showinfo("No Action", "Enter at least one Homefill quantity to add.")
            return
        self.state["output"] += qty
        self.state["weighted_output"] += HOMEFILL_POINTS * qty
        self.state["count_homefill_flat"] = self.state.get("count_homefill_flat", 0) + h_flat
        self.state["count_homefill_manuf"] = self.state.get("count_homefill_manuf", 0) + h_manuf
        self.state["count_homefill"] = self.state.get("count_homefill", 0) + qty
        save_progress(self.state)
        self._refresh_totals()
        messagebox.showinfo("Added", f"Added {qty} Homefill unit(s).")

    def _add_525(self):
        q = self._parse_nonneg(self.add_q)
        p = self._parse_nonneg(self.add_p)
        m = self._parse_nonneg(self.add_m)
        f = self._parse_nonneg(self.add_f)
        w = self._parse_nonneg(self.add_w)
        total = q + p + m + f + w
        if total == 0:
            messagebox.showinfo("No Action", "Enter at least one quantity to add.")
            return
        self.state["output"] += total
        self.state["weighted_output"] += (
            DEV_POINTS["QM Warranty"] * q
            + DEV_POINTS["PM"] * p
            + DEV_POINTS["Minor Repair"] * m
            + DEV_POINTS["Flat Rate"] * f
            + DEV_POINTS["Manufacture Warranty"] * w
        )
        self.state["count_qm"] = self.state.get("count_qm", 0) + q
        self.state["count_pm"] = self.state.get("count_pm", 0) + p
        self.state["count_minor"] = self.state.get("count_minor", 0) + m
        self.state["count_flat"] = self.state.get("count_flat", 0) + f
        self.state["count_manuf"] = self.state.get("count_manuf", 0) + w
        save_progress(self.state)
        self._refresh_totals()
        messagebox.showinfo("Added", f"Added {total} unit(s) across 525 warranties.")

    def _add_1025(self):
        q = self._parse_nonneg(self.add10_q)
        p = self._parse_nonneg(self.add10_p)
        m = self._parse_nonneg(self.add10_m)
        f = self._parse_nonneg(self.add10_f)
        w = self._parse_nonneg(self.add10_w)
        total = q + p + m + f + w
        if total == 0:
            messagebox.showinfo("No Action", "Enter at least one quantity to add.")
            return
        self.state["output"] += total
        self.state["weighted_output"] += (
            DEV_POINTS["QM Warranty"] * q
            + DEV_POINTS["PM"] * p
            + DEV_POINTS["Minor Repair"] * m
            + DEV_POINTS["Flat Rate"] * f
            + DEV_POINTS["Manufacture Warranty"] * w
        )
        self.state["count_1025_qm"] = self.state.get("count_1025_qm", 0) + q
        self.state["count_1025_pm"] = self.state.get("count_1025_pm", 0) + p
        self.state["count_1025_minor"] = self.state.get("count_1025_minor", 0) + m
        self.state["count_1025_flat"] = self.state.get("count_1025_flat", 0) + f
        self.state["count_1025_manuf"] = self.state.get("count_1025_manuf", 0) + w
        save_progress(self.state)
        self._refresh_totals()
        messagebox.showinfo("Added", f"Added {total} unit(s) across 1025 warranties.")

    # ---- Remove handlers ----
    def _remove_stratus(self):
        if self.state["output"] == 0:
            messagebox.showwarning("No Units", "No units to remove.")
            return
        s_flat = self._parse_nonneg(self.rem_s_flat)
        s_manuf = self._parse_nonneg(self.rem_s_manuf)
        qty = s_flat + s_manuf
        if qty == 0:
            messagebox.showinfo("No Action", "Enter at least one Stratus quantity to remove.")
            return
        if qty > self.state["output"]:
            messagebox.showwarning("Too Many", "Cannot remove more than total output.")
            return
        if s_flat > self.state.get("count_stratus_flat", 0):
            messagebox.showwarning("Too Many", "Cannot remove more Stratus Flat Rate than recorded.")
            return
        if s_manuf > self.state.get("count_stratus_manuf", 0):
            messagebox.showwarning("Too Many", "Cannot remove more Stratus Manufacture Warranty than recorded.")
            return
        self.state["output"] -= qty
        self.state["weighted_output"] -= STRATUS_POINTS * qty
        self.state["count_stratus_flat"] -= s_flat
        self.state["count_stratus_manuf"] -= s_manuf
        self.state["count_stratus"] -= qty
        if self.state["output"] == 0:
            self.state["weighted_output"] = 0.0
        save_progress(self.state)
        self._refresh_totals()
        messagebox.showinfo("Removed", f"Removed {qty} Stratus unit(s).")

    def _remove_homefill(self):
        if self.state["output"] == 0:
            messagebox.showwarning("No Units", "No units to remove.")
            return
        h_flat = self._parse_nonneg(self.rem_h_flat)
        h_manuf = self._parse_nonneg(self.rem_h_manuf)
        qty = h_flat + h_manuf
        if qty == 0:
            messagebox.showinfo("No Action", "Enter at least one Homefill quantity to remove.")
            return
        if qty > self.state["output"]:
            messagebox.showwarning("Too Many", "Cannot remove more than total output.")
            return
        if h_flat > self.state.get("count_homefill_flat", 0):
            messagebox.showwarning("Too Many", "Cannot remove more Homefill Flat Rate than recorded.")
            return
        if h_manuf > self.state.get("count_homefill_manuf", 0):
            messagebox.showwarning("Too Many", "Cannot remove more Homefill Manufacture Warranty than recorded.")
            return
        self.state["output"] -= qty
        self.state["weighted_output"] -= HOMEFILL_POINTS * qty
        self.state["count_homefill_flat"] -= h_flat
        self.state["count_homefill_manuf"] -= h_manuf
        self.state["count_homefill"] -= qty
        if self.state["output"] == 0:
            self.state["weighted_output"] = 0.0
        save_progress(self.state)
        self._refresh_totals()
        messagebox.showinfo("Removed", f"Removed {qty} Homefill unit(s).")

    def _remove_525(self):
        if self.state["output"] == 0:
            messagebox.showwarning("No Units", "No units to remove.")
            return
        q = self._parse_nonneg(self.rem_q)
        p = self._parse_nonneg(self.rem_p)
        m = self._parse_nonneg(self.rem_m)
        f = self._parse_nonneg(self.rem_f)
        w = self._parse_nonneg(self.rem_w)
        total = q + p + m + f + w
        if total == 0:
            messagebox.showinfo("No Action", "Enter at least one quantity to remove.")
            return
        if total > self.state["output"]:
            messagebox.showwarning("Too Many", "Cannot remove more than total output.")
            return
        # per-category checks
        if q > self.state.get("count_qm", 0):
            messagebox.showwarning("Too Many", "Cannot remove more QM Warranty than recorded.")
            return
        if p > self.state.get("count_pm", 0):
            messagebox.showwarning("Too Many", "Cannot remove more PM than recorded.")
            return
        if m > self.state.get("count_minor", 0):
            messagebox.showwarning("Too Many", "Cannot remove more Minor Repair than recorded.")
            return
        if f > self.state.get("count_flat", 0):
            messagebox.showwarning("Too Many", "Cannot remove more Flat Rate than recorded.")
            return
        if w > self.state.get("count_manuf", 0):
            messagebox.showwarning("Too Many", "Cannot remove more Manufacture Warranty than recorded.")
            return
        self.state["output"] -= total
        self.state["weighted_output"] -= (
            DEV_POINTS["QM Warranty"] * q
            + DEV_POINTS["PM"] * p
            + DEV_POINTS["Minor Repair"] * m
            + DEV_POINTS["Flat Rate"] * f
            + DEV_POINTS["Manufacture Warranty"] * w
        )
        self.state["count_qm"] -= q
        self.state["count_pm"] -= p
        self.state["count_minor"] -= m
        self.state["count_flat"] -= f
        self.state["count_manuf"] -= w
        if self.state["output"] == 0:
            self.state["weighted_output"] = 0.0
        save_progress(self.state)
        self._refresh_totals()
        messagebox.showinfo("Removed", f"Removed {total} unit(s) across 525 warranties.")

    def _remove_1025(self):
        if self.state["output"] == 0:
            messagebox.showwarning("No Units", "No units to remove.")
            return
        q = self._parse_nonneg(self.rem10_q)
        p = self._parse_nonneg(self.rem10_p)
        m = self._parse_nonneg(self.rem10_m)
        f = self._parse_nonneg(self.rem10_f)
        w = self._parse_nonneg(self.rem10_w)
        total = q + p + m + f + w
        if total == 0:
            messagebox.showinfo("No Action", "Enter at least one quantity to remove.")
            return
        if total > self.state["output"]:
            messagebox.showwarning("Too Many", "Cannot remove more than total output.")
            return
        # per-category checks
        if q > self.state.get("count_1025_qm", 0) or \
           p > self.state.get("count_1025_pm", 0) or \
           m > self.state.get("count_1025_minor", 0) or \
           f > self.state.get("count_1025_flat", 0) or \
           w > self.state.get("count_1025_manuf", 0):
            messagebox.showwarning("Too Many", "Cannot remove more than recorded for 1025 categories.")
            return
        self.state["output"] -= total
        self.state["weighted_output"] -= (
            DEV_POINTS["QM Warranty"] * q
            + DEV_POINTS["PM"] * p
            + DEV_POINTS["Minor Repair"] * m
            + DEV_POINTS["Flat Rate"] * f
            + DEV_POINTS["Manufacture Warranty"] * w
        )
        self.state["count_1025_qm"] -= q
        self.state["count_1025_pm"] -= p
        self.state["count_1025_minor"] -= m
        self.state["count_1025_flat"] -= f
        self.state["count_1025_manuf"] -= w
        if self.state["output"] == 0:
            self.state["weighted_output"] = 0.0
        save_progress(self.state)
        self._refresh_totals()
        messagebox.showinfo("Removed", f"Removed {total} unit(s) across 1025 warranties.")

    # ---- breakdown tab ----
    def _build_breakdown_tab(self, parent):
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)
        grid = ttk.Frame(parent)
        grid.grid(row=0, column=0, sticky="nw")
        table_frame = ttk.Frame(parent)
        table_frame.grid(row=0, column=1, sticky="ne", padx=(16,0))

        self.bd_labels = {}
        self.bd_title_vars = {}
        row = 0

        # Stratus total (bold)
        title_stratus = tk.StringVar(value="Stratus:")
        ttk.Label(grid, textvariable=title_stratus, font=self.bold_font).grid(row=row, column=0, sticky="w", pady=2)
        var_stratus = tk.StringVar()
        ttk.Label(grid, textvariable=var_stratus, font=self.bold_font).grid(row=row, column=1, sticky="w")
        self.bd_labels["count_stratus"] = var_stratus
        self.bd_title_vars["title_stratus"] = title_stratus
        row += 1
        # Stratus subcategories
        title_s_flat = tk.StringVar(value="Stratus Flat Rate:")
        ttk.Label(grid, textvariable=title_s_flat).grid(row=row, column=0, sticky="w", pady=2)
        var_s_flat = tk.StringVar()
        ttk.Label(grid, textvariable=var_s_flat).grid(row=row, column=1, sticky="w")
        self.bd_labels["count_stratus_flat"] = var_s_flat
        self.bd_title_vars["title_stratus_flat"] = title_s_flat
        row += 1
        title_s_manuf = tk.StringVar(value="Stratus Manufacture Warranty:")
        ttk.Label(grid, textvariable=title_s_manuf).grid(row=row, column=0, sticky="w", pady=2)
        var_s_manuf = tk.StringVar()
        ttk.Label(grid, textvariable=var_s_manuf).grid(row=row, column=1, sticky="w")
        self.bd_labels["count_stratus_manuf"] = var_s_manuf
        self.bd_title_vars["title_stratus_manuf"] = title_s_manuf
        row += 1

        # Homefill total (bold)
        title_homefill = tk.StringVar(value="Homefill:")
        ttk.Label(grid, textvariable=title_homefill, font=self.bold_font).grid(row=row, column=0, sticky="w", pady=(8,2))
        var_homefill = tk.StringVar()
        ttk.Label(grid, textvariable=var_homefill, font=self.bold_font).grid(row=row, column=1, sticky="w")
        self.bd_labels["count_homefill"] = var_homefill
        self.bd_title_vars["title_homefill"] = title_homefill
        row += 1
        # Homefill subcategories
        title_h_flat = tk.StringVar(value="Homefill Flat Rate:")
        ttk.Label(grid, textvariable=title_h_flat).grid(row=row, column=0, sticky="w", pady=2)
        var_h_flat = tk.StringVar()
        ttk.Label(grid, textvariable=var_h_flat).grid(row=row, column=1, sticky="w")
        self.bd_labels["count_homefill_flat"] = var_h_flat
        self.bd_title_vars["title_homefill_flat"] = title_h_flat
        row += 1
        title_h_manuf = tk.StringVar(value="Homefill Manufacture Warranty:")
        ttk.Label(grid, textvariable=title_h_manuf).grid(row=row, column=0, sticky="w", pady=2)
        var_h_manuf = tk.StringVar()
        ttk.Label(grid, textvariable=var_h_manuf).grid(row=row, column=1, sticky="w")
        self.bd_labels["count_homefill_manuf"] = var_h_manuf
        self.bd_title_vars["title_homefill_manuf"] = title_h_manuf
        row += 1

        # 525 total (bold)
        title_525 = tk.StringVar(value="525:")
        ttk.Label(grid, textvariable=title_525, font=self.bold_font).grid(row=row, column=0, sticky="w", pady=(8,2))
        var_525_total = tk.StringVar()
        ttk.Label(grid, textvariable=var_525_total, font=self.bold_font).grid(row=row, column=1, sticky="w")
        self.bd_labels["total_525"] = var_525_total
        self.bd_title_vars["title_525"] = title_525
        row += 1
        # 525 subcategories
        for title, key in [
            ("525 QM Warranty", "count_qm"),
            ("525 PM", "count_pm"),
            ("525 Minor Repair", "count_minor"),
            ("525 Flat Rate", "count_flat"),
            ("525 Manufacture Warranty", "count_manuf"),
        ]:
            tvar = tk.StringVar(value=f"{title}:")
            ttk.Label(grid, textvariable=tvar).grid(row=row, column=0, sticky="w", pady=2)
            var = tk.StringVar()
            ttk.Label(grid, textvariable=var).grid(row=row, column=1, sticky="w")
            self.bd_labels[key] = var
            # map title vars by suffix for easy refresh
            suffix = key.split("_")[-1]
            self.bd_title_vars[f"title_525_{suffix}"] = tvar
            row += 1

        # 1025 total (bold)
        title_1025 = tk.StringVar(value="1025:")
        ttk.Label(grid, textvariable=title_1025, font=self.bold_font).grid(row=row, column=0, sticky="w", pady=(8,2))
        var_1025_total = tk.StringVar()
        ttk.Label(grid, textvariable=var_1025_total, font=self.bold_font).grid(row=row, column=1, sticky="w")
        self.bd_labels["total_1025"] = var_1025_total
        self.bd_title_vars["title_1025"] = title_1025
        row += 1
        # 1025 subcategories
        for title, key in [
            ("1025 QM Warranty", "count_1025_qm"),
            ("1025 PM", "count_1025_pm"),
            ("1025 Minor Repair", "count_1025_minor"),
            ("1025 Flat Rate", "count_1025_flat"),
            ("1025 Manufacture Warranty", "count_1025_manuf"),
        ]:
            tvar = tk.StringVar(value=f"{title}:")
            ttk.Label(grid, textvariable=tvar).grid(row=row, column=0, sticky="w", pady=2)
            var = tk.StringVar()
            ttk.Label(grid, textvariable=var).grid(row=row, column=1, sticky="w")
            self.bd_labels[key] = var
            # map title vars by 1025 suffix
            suffix = key.split("_")[-1]
            self.bd_title_vars[f"title_1025_{suffix}"] = tvar
            row += 1

        # Right-side table: points structure
        self._build_points_table(table_frame)

        self._refresh_breakdown()

    def _refresh_breakdown(self):
        # Stratus
        self.bd_labels["count_stratus"].set(str(self.state.get("count_stratus", 0)))
        self.bd_labels["count_stratus_flat"].set(str(self.state.get("count_stratus_flat", 0)))
        self.bd_labels["count_stratus_manuf"].set(str(self.state.get("count_stratus_manuf", 0)))
        # Stratus points in titles
        s_total = self.state.get("count_stratus", 0)
        s_flat = self.state.get("count_stratus_flat", 0)
        s_manuf = self.state.get("count_stratus_manuf", 0)
        self.bd_title_vars["title_stratus"].set(f"Stratus ({STRATUS_POINTS * s_total:.2f} pts):")
        self.bd_title_vars["title_stratus_flat"].set(f"Stratus Flat Rate ({STRATUS_POINTS * s_flat:.2f} pts):")
        self.bd_title_vars["title_stratus_manuf"].set(f"Stratus Manufacture Warranty ({STRATUS_POINTS * s_manuf:.2f} pts):")
        # Homefill
        self.bd_labels["count_homefill"].set(str(self.state.get("count_homefill", 0)))
        self.bd_labels["count_homefill_flat"].set(str(self.state.get("count_homefill_flat", 0)))
        self.bd_labels["count_homefill_manuf"].set(str(self.state.get("count_homefill_manuf", 0)))
        # Homefill points in titles
        h_total = self.state.get("count_homefill", 0)
        h_flat = self.state.get("count_homefill_flat", 0)
        h_manuf = self.state.get("count_homefill_manuf", 0)
        self.bd_title_vars["title_homefill"].set(f"Homefill ({HOMEFILL_POINTS * h_total:.2f} pts):")
        self.bd_title_vars["title_homefill_flat"].set(f"Homefill Flat Rate ({HOMEFILL_POINTS * h_flat:.2f} pts):")
        self.bd_title_vars["title_homefill_manuf"].set(f"Homefill Manufacture Warranty ({HOMEFILL_POINTS * h_manuf:.2f} pts):")
        # 525 total and subcats
        qm = self.state.get("count_qm", 0)
        pm = self.state.get("count_pm", 0)
        minor = self.state.get("count_minor", 0)
        flat = self.state.get("count_flat", 0)
        manuf = self.state.get("count_manuf", 0)
        total_525 = qm + pm + minor + flat + manuf
        self.bd_labels["total_525"].set(str(total_525))
        self.bd_labels["count_qm"].set(str(qm))
        self.bd_labels["count_pm"].set(str(pm))
        self.bd_labels["count_minor"].set(str(minor))
        self.bd_labels["count_flat"].set(str(flat))
        self.bd_labels["count_manuf"].set(str(manuf))
        # 525 points in titles
        pts_525_total = (
            DEV_POINTS["QM Warranty"] * qm
            + DEV_POINTS["PM"] * pm
            + DEV_POINTS["Minor Repair"] * minor
            + DEV_POINTS["Flat Rate"] * flat
            + DEV_POINTS["Manufacture Warranty"] * manuf
        )
        self.bd_title_vars["title_525"].set(f"525 ({pts_525_total:.2f} pts):")
        self.bd_title_vars["title_525_qm"].set(f"525 QM Warranty ({DEV_POINTS['QM Warranty'] * qm:.2f} pts):")
        self.bd_title_vars["title_525_pm"].set(f"525 PM ({DEV_POINTS['PM'] * pm:.2f} pts):")
        self.bd_title_vars["title_525_minor"].set(f"525 Minor Repair ({DEV_POINTS['Minor Repair'] * minor:.2f} pts):")
        self.bd_title_vars["title_525_flat"].set(f"525 Flat Rate ({DEV_POINTS['Flat Rate'] * flat:.2f} pts):")
        self.bd_title_vars["title_525_manuf"].set(f"525 Manufacture Warranty ({DEV_POINTS['Manufacture Warranty'] * manuf:.2f} pts):")
        # 1025 total and subcats
        q10 = self.state.get("count_1025_qm", 0)
        p10 = self.state.get("count_1025_pm", 0)
        m10 = self.state.get("count_1025_minor", 0)
        f10 = self.state.get("count_1025_flat", 0)
        w10 = self.state.get("count_1025_manuf", 0)
        total_1025 = q10 + p10 + m10 + f10 + w10
        self.bd_labels["total_1025"].set(str(total_1025))
        self.bd_labels["count_1025_qm"].set(str(q10))
        self.bd_labels["count_1025_pm"].set(str(p10))
        self.bd_labels["count_1025_minor"].set(str(m10))
        self.bd_labels["count_1025_flat"].set(str(f10))
        self.bd_labels["count_1025_manuf"].set(str(w10))
        # 1025 points in titles
        pts_1025_total = (
            DEV_POINTS["QM Warranty"] * q10
            + DEV_POINTS["PM"] * p10
            + DEV_POINTS["Minor Repair"] * m10
            + DEV_POINTS["Flat Rate"] * f10
            + DEV_POINTS["Manufacture Warranty"] * w10
        )
        self.bd_title_vars["title_1025"].set(f"1025 ({pts_1025_total:.2f} pts):")
        self.bd_title_vars["title_1025_qm"].set(f"1025 QM Warranty ({DEV_POINTS['QM Warranty'] * q10:.2f} pts):")
        self.bd_title_vars["title_1025_pm"].set(f"1025 PM ({DEV_POINTS['PM'] * p10:.2f} pts):")
        self.bd_title_vars["title_1025_minor"].set(f"1025 Minor Repair ({DEV_POINTS['Minor Repair'] * m10:.2f} pts):")
        self.bd_title_vars["title_1025_flat"].set(f"1025 Flat Rate ({DEV_POINTS['Flat Rate'] * f10:.2f} pts):")
        self.bd_title_vars["title_1025_manuf"].set(f"1025 Manufacture Warranty ({DEV_POINTS['Manufacture Warranty'] * w10:.2f} pts):")

    def _build_points_table(self, parent):
        cols = ("Unit", "Warranty", "Pts/unit")
        tree = ttk.Treeview(parent, columns=cols, show="headings", height=18)
        for c in cols:
            tree.heading(c, text=c)
        # Set column widths moderately
        tree.column("Unit", width=110, anchor="w")
        tree.column("Warranty", width=180, anchor="w")
        tree.column("Pts/unit", width=90, anchor="center")

        # Data rows describing the points structure
        rows = [
            ("Stratus", "Flat Rate", f"{STRATUS_POINTS:.2f}"),
            ("Stratus", "Manufacture Warranty", f"{STRATUS_POINTS:.2f}"),
            ("Homefill", "Flat Rate", f"{HOMEFILL_POINTS:.2f}"),
            ("Homefill", "Manufacture Warranty", f"{HOMEFILL_POINTS:.2f}"),
            ("525", "QM Warranty", f"{DEV_POINTS['QM Warranty']:.2f}"),
            ("525", "PM", f"{DEV_POINTS['PM']:.2f}"),
            ("525", "Minor Repair", f"{DEV_POINTS['Minor Repair']:.2f}"),
            ("525", "Flat Rate", f"{DEV_POINTS['Flat Rate']:.2f}"),
            ("525", "Manufacture Warranty", f"{DEV_POINTS['Manufacture Warranty']:.2f}"),
            ("1025", "QM Warranty", f"{DEV_POINTS['QM Warranty']:.2f}"),
            ("1025", "PM", f"{DEV_POINTS['PM']:.2f}"),
            ("1025", "Minor Repair", f"{DEV_POINTS['Minor Repair']:.2f}"),
            ("1025", "Flat Rate", f"{DEV_POINTS['Flat Rate']:.2f}"),
            ("1025", "Manufacture Warranty", f"{DEV_POINTS['Manufacture Warranty']:.2f}"),
        ]
        for r in rows:
            tree.insert("", "end", values=r)
        ttk.Label(parent, text="Points by Unit + Warranty", font=self.bold_font).grid(row=0, column=0, sticky="w", pady=(0,6))
        tree.grid(row=1, column=0, sticky="nsew")
        parent.rowconfigure(1, weight=1)

    def _open_edit_breakdown(self):
        total = self.state.get("output", 0)
        win = tk.Toplevel(self)
        win.title("Edit Breakdown")
        win.transient(self)
        win.grab_set()

        ttk.Label(win, text=f"Total output: {total}").grid(row=0, column=0, columnspan=2, sticky="w", pady=(8,4))

        entries = {}
        fields = [
            ("Stratus Flat Rate", "count_stratus_flat"),
            ("Stratus Manufacture Warranty", "count_stratus_manuf"),
            ("Homefill Flat Rate", "count_homefill_flat"),
            ("Homefill Manufacture Warranty", "count_homefill_manuf"),
            ("525 QM Warranty", "count_qm"),
            ("525 PM", "count_pm"),
            ("525 Minor Repair", "count_minor"),
            ("525 Flat Rate", "count_flat"),
            ("525 Manufacture Warranty", "count_manuf"),
            ("1025 QM Warranty", "count_1025_qm"),
            ("1025 PM", "count_1025_pm"),
            ("1025 Minor Repair", "count_1025_minor"),
            ("1025 Flat Rate", "count_1025_flat"),
            ("1025 Manufacture Warranty", "count_1025_manuf"),
        ]
        for i, (label, key) in enumerate(fields, start=1):
            ttk.Label(win, text=label+":").grid(row=i, column=0, sticky="w")
            var = tk.StringVar(value=str(self.state.get(key, 0)))
            e = ttk.Entry(win, textvariable=var, width=10)
            e.grid(row=i, column=1, sticky="w")
            entries[key] = var

        status = tk.StringVar(value="Enter non-negative integers that sum to total.")
        ttk.Label(win, textvariable=status, foreground="#555").grid(row=len(fields)+1, column=0, columnspan=2, sticky="w", pady=(6,6))

        def on_save():
            try:
                s_flat = int(entries["count_stratus_flat"].get().strip())
                s_manuf = int(entries["count_stratus_manuf"].get().strip())
                h_flat = int(entries["count_homefill_flat"].get().strip())
                h_manuf = int(entries["count_homefill_manuf"].get().strip())
                q = int(entries["count_qm"].get().strip())
                p = int(entries["count_pm"].get().strip())
                m = int(entries["count_minor"].get().strip())
                f = int(entries["count_flat"].get().strip())
                w = int(entries["count_manuf"].get().strip())
                q10 = int(entries["count_1025_qm"].get().strip())
                p10 = int(entries["count_1025_pm"].get().strip())
                m10 = int(entries["count_1025_minor"].get().strip())
                f10 = int(entries["count_1025_flat"].get().strip())
                w10 = int(entries["count_1025_manuf"].get().strip())
            except Exception:
                messagebox.showerror("Invalid", "All fields must be integers.")
                return
            if any(x < 0 for x in (s_flat,s_manuf,h_flat,h_manuf,q,p,m,f,w,q10,p10,m10,f10,w10)):
                messagebox.showerror("Invalid", "Values must be non-negative.")
                return
            s = s_flat + s_manuf
            h = h_flat + h_manuf
            ssum = s + h + q + p + m + f + w + q10 + p10 + m10 + f10 + w10
            if ssum != total:
                messagebox.showerror("Sum Mismatch", f"Sum of entries ({ssum}) must equal total output ({total}).")
                return
            # Commit
            self.state["count_stratus"] = s
            self.state["count_stratus_flat"] = s_flat
            self.state["count_stratus_manuf"] = s_manuf
            self.state["count_homefill"] = h
            self.state["count_homefill_flat"] = h_flat
            self.state["count_homefill_manuf"] = h_manuf
            self.state["count_qm"] = q
            self.state["count_pm"] = p
            self.state["count_minor"] = m
            self.state["count_flat"] = f
            self.state["count_manuf"] = w
            self.state["count_1025_qm"] = q10
            self.state["count_1025_pm"] = p10
            self.state["count_1025_minor"] = m10
            self.state["count_1025_flat"] = f10
            self.state["count_1025_manuf"] = w10
            self.state["weighted_output"] = (
                STRATUS_POINTS * s
                + HOMEFILL_POINTS * h
                + DEV_POINTS["QM Warranty"] * q
                + DEV_POINTS["PM"] * p
                + DEV_POINTS["Minor Repair"] * m
                + DEV_POINTS["Flat Rate"] * f
                + DEV_POINTS["Manufacture Warranty"] * w
                + DEV_POINTS["QM Warranty"] * q10
                + DEV_POINTS["PM"] * p10
                + DEV_POINTS["Minor Repair"] * m10
                + DEV_POINTS["Flat Rate"] * f10
                + DEV_POINTS["Manufacture Warranty"] * w10
            )
            save_progress(self.state)
            self._refresh_totals()
            win.destroy()

        btns = ttk.Frame(win)
        btns.grid(row=len(fields)+2, column=0, columnspan=2, pady=(6,8))
        ttk.Button(btns, text="Save", command=on_save).grid(row=0, column=0, padx=(0,8))
        ttk.Button(btns, text="Cancel", command=win.destroy).grid(row=0, column=1)

    # ---- parsing helpers ----
    def _parse_nonneg(self, var: tk.StringVar) -> int:
        try:
            v = int(var.get().strip())
            return max(0, v)
        except Exception:
            return 0

    def _parse_pos(self, var: tk.StringVar):
        try:
            v = int(var.get().strip())
            if v > 0:
                return v
            return None
        except Exception:
            return None

    def _on_close(self):
        try:
            save_progress(self.state)
        finally:
            self.destroy()

    def _edit_today_output(self):
        win = tk.Toplevel(self)
        win.title("Edit Today's Output")
        win.transient(self)
        win.grab_set()

        current = max(0, self.state.get("output", 0) - self.state.get("start_of_day_output", 0))
        ttk.Label(win, text=f"Current value: {current}").grid(row=0, column=0, columnspan=2, sticky="w", pady=(8,4))
        ttk.Label(win, text="New value:").grid(row=1, column=0, sticky="w")
        var = tk.StringVar(value=str(current))
        entry = ttk.Entry(win, textvariable=var, width=10)
        entry.grid(row=1, column=1, sticky="w")

        status = tk.StringVar(value="Enter a non-negative integer.")
        ttk.Label(win, textvariable=status, foreground="#555").grid(row=2, column=0, columnspan=2, sticky="w", pady=(6,6))

        def on_save():
            try:
                val = int(var.get().strip())
            except Exception:
                messagebox.showerror("Invalid", "Value must be an integer.")
                return
            if val < 0:
                messagebox.showerror("Invalid", "Value must be non-negative.")
                return
            total = self.state.get("output", 0)
            # Adjust start_of_day_output so that today's output equals val
            new_start = total - val
            if new_start < 0:
                new_start = 0
            self.state["start_of_day_output"] = new_start
            save_progress(self.state)
            self._refresh_totals()
            win.destroy()

        btns = ttk.Frame(win)
        btns.grid(row=3, column=0, columnspan=2, pady=(6,8))
        ttk.Button(btns, text="Save", command=on_save).grid(row=0, column=0, padx=(0,8))
        ttk.Button(btns, text="Cancel", command=win.destroy).grid(row=0, column=1)

    def _edit_start_of_day(self):
        win = tk.Toplevel(self)
        win.title("Edit Started Today With")
        win.transient(self)
        win.grab_set()

        current = self.state.get("start_of_day_output", 0)
        ttk.Label(win, text=f"Current value: {current}").grid(row=0, column=0, columnspan=2, sticky="w", pady=(8,4))
        ttk.Label(win, text="New value:").grid(row=1, column=0, sticky="w")
        var = tk.StringVar(value=str(current))
        entry = ttk.Entry(win, textvariable=var, width=10)
        entry.grid(row=1, column=1, sticky="w")

        status = tk.StringVar(value="Enter a non-negative integer. Optional: ≤ current total output.")
        ttk.Label(win, textvariable=status, foreground="#555").grid(row=2, column=0, columnspan=2, sticky="w", pady=(6,6))

        def on_save():
            try:
                val = int(var.get().strip())
            except Exception:
                messagebox.showerror("Invalid", "Value must be an integer.")
                return
            if val < 0:
                messagebox.showerror("Invalid", "Value must be non-negative.")
                return
            # Optional guard: cannot exceed current output (can relax if desired)
            total = self.state.get("output", 0)
            if val > total:
                if not messagebox.askyesno("Confirm", f"Entered value ({val}) exceeds current total output ({total}). Save anyway?"):
                    return
            self.state["start_of_day_output"] = val
            save_progress(self.state)
            self._refresh_totals()
            win.destroy()

        btns = ttk.Frame(win)
        btns.grid(row=3, column=0, columnspan=2, pady=(6,8))
        ttk.Button(btns, text="Save", command=on_save).grid(row=0, column=0, padx=(0,8))
        ttk.Button(btns, text="Cancel", command=win.destroy).grid(row=0, column=1)


if __name__ == "__main__":
    app = WeightedOutputApp()
    app.mainloop()
