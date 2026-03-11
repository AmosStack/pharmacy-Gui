import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import re


class SalesMixin:

    @staticmethod
    def _row_value(row, key, index, default=None):
        if isinstance(row, dict):
            return row.get(key, default)
        if row is None:
            return default
        try:
            return row[index]
        except Exception:
            return default

    def build_sales_tab(self):
        frame = ttk.Frame(self.sales_tab, padding=20)
        frame.pack(fill="both", expand=True)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=3)
        frame.grid_columnconfigure(1, weight=2)

        self.cart = []
        self.ensure_sale_item_prescription_column()

        left_panel = ttk.Frame(frame)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

        form = ttk.LabelFrame(left_panel, text="Create Sale", padding=15)
        form.pack(fill="x", pady=10)

        ttk.Label(form, text="Patient").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.patient_combo = ttk.Combobox(form, width=35)
        self.patient_combo.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form, text="Medicine").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.sale_combo = ttk.Combobox(form, width=35)
        self.sale_combo.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form, text="Quantity").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.sale_qty = ttk.Entry(form, width=38)
        self.sale_qty.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form, text="Prescription (A*B*C)").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.prescription_entry = ttk.Entry(form, width=38)
        self.prescription_entry.grid(row=3, column=1, padx=5, pady=5)

        self.prescription_hint = ttk.Label(
            form,
            text="A = units, B = times/day, C = days",
            foreground="#0d6efd",
        )
        self.prescription_hint.grid(row=4, column=0, columnspan=2, sticky="w")

        self.sale_combo.bind("<<ComboboxSelected>>", self.update_prescription_hint)
        self.sale_combo.bind("<KeyRelease>", self.filter_medicines_for_sale)
        self.patient_combo.bind("<KeyRelease>", self.filter_patients_for_sale)
        self.patient_combo.bind("<Button-1>", lambda _e: self.load_patients_for_sale())

        tk.Button(
            form,
            text="Add to Cart",
            bg="#28a745",
            fg="white",
            width=20,
            command=self.add_item_to_cart,
        ).grid(row=5, column=0, columnspan=2, pady=10)

        history_frame = ttk.LabelFrame(left_panel, text="Sales History", padding=15)
        history_frame.pack(fill="both", expand=True)

        columns = ("ID", "Patient", "Date", "Prescription", "Total")
        self.sales_tree = ttk.Treeview(history_frame, columns=columns, show="headings")
        self.sales_tree.pack(fill="both", expand=True)

        for col in columns:
            self.sales_tree.heading(col, text=col)
            self.sales_tree.column(col, width=150)

        self.cart_panel = ttk.LabelFrame(frame, text="Cart", padding=10)
        self.cart_panel.grid(row=0, column=1, sticky="nsew")
        self.cart_panel.grid_rowconfigure(0, weight=1)
        self.cart_panel.grid_columnconfigure(0, weight=1)

        self.cart_canvas = tk.Canvas(self.cart_panel, highlightthickness=0)
        self.cart_scrollbar = ttk.Scrollbar(self.cart_panel, orient="vertical", command=self.cart_canvas.yview)
        self.cart_cards_frame = ttk.Frame(self.cart_canvas)
        self.cart_canvas_window = self.cart_canvas.create_window((0, 0), window=self.cart_cards_frame, anchor="nw")
        self.cart_canvas.configure(yscrollcommand=self.cart_scrollbar.set)

        self.cart_canvas.grid(row=0, column=0, sticky="nsew")
        self.cart_scrollbar.grid(row=0, column=1, sticky="ns")

        self.cart_cards_frame.bind("<Configure>", self._on_cart_cards_configure)
        self.cart_canvas.bind("<Configure>", self._on_cart_canvas_configure)

        self.cart_total_label = ttk.Label(self.cart_panel, text="Total: 0.00", font=("Arial", 11, "bold"))
        self.cart_total_label.grid(row=1, column=0, columnspan=2, sticky="ew", pady=8)

        cart_btn_frame = ttk.Frame(self.cart_panel)
        cart_btn_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=5)
        cart_btn_frame.columnconfigure(0, weight=1)
        cart_btn_frame.columnconfigure(1, weight=1)

        tk.Button(
            cart_btn_frame,
            text="Checkout",
            bg="#007bff",
            fg="white",
            width=16,
            command=self.finalize_sale,
        ).grid(row=0, column=0, padx=5, sticky="ew")

        tk.Button(
            cart_btn_frame,
            text="Clear",
            bg="#dc3545",
            fg="white",
            width=16,
            command=self.clear_cart,
        ).grid(row=0, column=1, padx=5, sticky="ew")

        self.refresh_cart_panel()
        if hasattr(self, "root") and self.root.winfo_exists():
            self.root.after(10, self._load_sales_initial_data)
        else:
            self._load_sales_initial_data()

    def _load_sales_initial_data(self):
        self.load_medicines_for_sale()
        self.load_patients_for_sale()
        self.refresh_sales_tab()

    def ensure_sale_item_prescription_column(self):
        try:
            self.cursor.execute("SHOW COLUMNS FROM sale_items LIKE 'prescription'")
            has_prescription = self.cursor.fetchone() is not None
            if not has_prescription:
                self.cursor.execute("ALTER TABLE sale_items ADD COLUMN prescription VARCHAR(255)")
                self.conn.commit()
        except Exception:
            self.conn.rollback()

    def toggle_cart_panel(self, show=None):
        if hasattr(self, "cart_panel") and self.cart_panel.winfo_exists():
            self.cart_panel.grid()
            self.refresh_cart_panel()

    def _on_cart_cards_configure(self, _event=None):
        if hasattr(self, "cart_canvas") and self.cart_canvas.winfo_exists():
            self.cart_canvas.configure(scrollregion=self.cart_canvas.bbox("all"))

    def _on_cart_canvas_configure(self, event):
        if hasattr(self, "cart_canvas_window"):
            self.cart_canvas.itemconfigure(self.cart_canvas_window, width=event.width)

    def refresh_cart_panel(self):
        if not hasattr(self, "cart_cards_frame"):
            return

        for card in self.cart_cards_frame.winfo_children():
            card.destroy()

        for idx, item in enumerate(self.cart):
            med = item["medicine"]
            dosage = item.get("dosage")
            dosage_text = f"{dosage[0]}*{dosage[1]}*{dosage[2]}" if dosage else "-"
            expiry = med.get("expiry_date")
            expiry_text = str(expiry) if expiry else "N/A"

            card = ttk.LabelFrame(self.cart_cards_frame, text=f"{idx + 1}. {med['name']}", padding=8)
            card.pack(fill="x", pady=6)

            details = (
                f"Type: {med.get('type', '-')}",
                f"Price: {med['price']:.2f}",
                f"Requested Qty: {item['quantity']}",
                f"Available Stock: {med.get('quantity', 0)}",
                f"Earliest Expiry: {expiry_text}",
                f"Prescription: {item.get('prescription', '-')}",
                f"Dosage A*B*C: {dosage_text}",
                f"Subtotal: {item['subtotal']:.2f}",
            )

            for line in details:
                ttk.Label(card, text=line, anchor="w").pack(fill="x")

            tk.Button(
                card,
                text="Remove",
                bg="#ffc107",
                width=10,
                command=lambda row_index=idx: self.remove_cart_item(row_index),
            ).pack(anchor="e", pady=(6, 0))

        total = sum(item["subtotal"] for item in self.cart)
        if hasattr(self, "cart_total_label"):
            self.cart_total_label.config(text=f"Total: {total:.2f}")

    def remove_cart_item(self, index):
        if 0 <= index < len(self.cart):
            self.cart.pop(index)
            self.refresh_cart_panel()

    def add_item_to_cart(self):
        med_name = self.sale_combo.get().strip()
        qty_text = self.sale_qty.get().strip()
        prescription_text = self.prescription_entry.get().strip()

        if not med_name or not qty_text:
            messagebox.showerror("Error", "Medicine and quantity required")
            return

        try:
            quantity = int(qty_text)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a positive integer.")
            return

        med = self.medicine_map.get(med_name)
        if not med or med["quantity"] <= 0:
            messagebox.showerror("Error", "Medicine not available or out of stock.")
            return

        if not prescription_text:
            messagebox.showerror("Error", "Prescription required (A*B*C).")
            return

        dosage = self.parse_prescription(prescription_text)
        if dosage is None:
            messagebox.showerror("Error", "Invalid prescription format A*B*C")
            return

        existing_qty = sum(
            item["quantity"]
            for item in self.cart
            if item["medicine"].get("group_key") == med.get("group_key")
        )
        if existing_qty + quantity > med["quantity"]:
            messagebox.showerror("Error", f"Only {med['quantity'] - existing_qty} left in stock")
            return

        for item in self.cart:
            if (
                item["medicine"].get("group_key") == med.get("group_key")
                and item["prescription"] == prescription_text
            ):
                item["quantity"] += quantity
                item["subtotal"] = item["quantity"] * med["price"]
                break
        else:
            self.cart.append(
                {
                    "medicine": med,
                    "quantity": quantity,
                    "subtotal": quantity * med["price"],
                    "prescription": prescription_text,
                    "dosage": dosage,
                }
            )

        self.sale_qty.delete(0, tk.END)
        self.prescription_entry.delete(0, tk.END)
        self.refresh_cart_panel()
        self.toggle_cart_panel()

    def parse_prescription(self, text):
        match = re.fullmatch(r"\s*(\d+)\*(\d+)\*(\d+)\s*", text)
        if not match:
            return None
        a, b, c = map(int, match.groups())
        if a <= 0 or b <= 0 or c <= 0:
            return None
        return a, b, c

    def update_prescription_hint(self, event=None):
        med_name = self.sale_combo.get().strip()
        med = self.medicine_map.get(med_name)
        med_type = (med.get("type") or "").lower() if med else ""

        if med_type in ("tablet", "capsule"):
            unit = "tabs/caps"
        elif med_type == "syrup":
            unit = "ml"
        else:
            unit = "units"

        self.prescription_hint.config(text=f"A = {unit}, B = times/day, C = days")

    def clear_cart(self):
        self.cart = []
        self.refresh_cart_panel()

    def finalize_sale(self):
        if not self.cart:
            messagebox.showerror("Error", "Cart is empty")
            return

        patient_name = self.patient_combo.get().strip()
        patient = self.patient_map.get(patient_name)
        if not patient:
            messagebox.showerror("Error", "Please select a valid patient")
            return

        try:
            allocations = []
            total = 0.0

            for item in self.cart:
                med = item["medicine"]
                required = item["quantity"]
                self.cursor.execute(
                    """
                    SELECT id, name, type, price, quantity, expiry_date
                    FROM medicines
                    WHERE name = %s AND type = %s AND quantity > 0
                    ORDER BY expiry_date IS NULL, expiry_date ASC, id ASC
                    """,
                    (med["name"], med["type"]),
                )
                batches = self.cursor.fetchall()

                remaining = required
                item_allocations = []
                for batch in batches:
                    if remaining <= 0:
                        break
                    available = self._row_value(batch, "quantity", 4, 0)
                    if available <= 0:
                        continue
                    take_qty = min(remaining, available)
                    line_subtotal = take_qty * float(self._row_value(batch, "price", 3, 0.0))
                    item_allocations.append(
                        {
                            "medicine_id": self._row_value(batch, "id", 0),
                            "quantity": take_qty,
                            "subtotal": line_subtotal,
                            "prescription": item.get("prescription"),
                        }
                    )
                    total += line_subtotal
                    remaining -= take_qty

                if remaining > 0:
                    raise ValueError(f"Insufficient stock for {med['name']}")

                allocations.extend(item_allocations)

            self.cursor.execute(
                "INSERT INTO sales (sale_date, total_amount, patient_id) VALUES (%s, %s, %s)",
                (date.today(), total, patient["id"]),
            )
            sale_id = self.cursor.lastrowid

            for alloc in allocations:
                self.cursor.execute(
                    "UPDATE medicines SET quantity = quantity - %s WHERE id=%s",
                    (alloc["quantity"], alloc["medicine_id"]),
                )
                self.cursor.execute(
                    "INSERT INTO sale_items (sale_id, medicine_id, quantity, subtotal, prescription) VALUES (%s, %s, %s, %s, %s)",
                    (
                        sale_id,
                        alloc["medicine_id"],
                        alloc["quantity"],
                        alloc["subtotal"],
                        alloc["prescription"],
                    ),
                )

            self.conn.commit()
            self.cart = []
            self.refresh_cart_panel()
            self.load_medicines_for_sale()
            self.refresh_sales_tab()
            if hasattr(self, "tree") and self.tree.winfo_exists() and hasattr(self, "load_inventory"):
                self.load_inventory()
            messagebox.showinfo("Success", "Sale completed successfully")
        except Exception as exc:
            self.conn.rollback()
            messagebox.showerror("Error", str(exc))

    def load_medicines_for_sale(self):
        self.medicine_map = {}
        self.medicine_batches_by_group = {}
        self.all_medicine_names = []

        self.cursor.execute(
            """
            SELECT id, name, type, price, quantity, expiry_date
            FROM medicines
            WHERE quantity > 0
            ORDER BY name ASC, expiry_date IS NULL, expiry_date ASC, id ASC
            """
        )
        for med in self.cursor.fetchall():
            med_name = self._row_value(med, "name", 1)
            med_type = self._row_value(med, "type", 2) or "Unknown"
            group_key = f"{med_name}||{med_type}"
            display_name = f"{med_name} - {med_type}"
            med_dict = {
                "id": self._row_value(med, "id", 0),
                "name": med_name,
                "type": med_type,
                "price": float(self._row_value(med, "price", 3, 0.0)),
                "quantity": int(self._row_value(med, "quantity", 4, 0)),
                "expiry_date": self._row_value(med, "expiry_date", 5),
            }
            if group_key not in self.medicine_batches_by_group:
                self.medicine_batches_by_group[group_key] = {
                    "display_name": display_name,
                    "batches": [],
                }
                self.all_medicine_names.append(display_name)
            self.medicine_batches_by_group[group_key]["batches"].append(med_dict)

        for group_key, bundle in self.medicine_batches_by_group.items():
            batches = bundle["batches"]
            first = batches[0]
            total_qty = sum(batch["quantity"] for batch in batches)
            self.medicine_map[bundle["display_name"]] = {
                "id": first["id"],
                "name": first["name"],
                "type": first["type"],
                "price": first["price"],
                "quantity": total_qty,
                "expiry_date": first.get("expiry_date"),
                "batch_count": len(batches),
                "group_key": group_key,
            }

        self.sale_combo["values"] = tuple(self.all_medicine_names)

    def load_patients_for_sale(self):
        self.patient_map = {}
        self.all_patient_names = []

        self.cursor.execute("SELECT id, name FROM patients")
        for pat in self.cursor.fetchall():
            patient_id = self._row_value(pat, "id", 0)
            patient_name = self._row_value(pat, "name", 1)
            self.patient_map[patient_name] = {"id": patient_id, "name": patient_name}
            self.all_patient_names.append(patient_name)

        self.patient_combo["values"] = tuple(self.all_patient_names)

    def filter_medicines_for_sale(self, event=None):
        query = self.sale_combo.get().strip().lower()
        if not query:
            self.sale_combo["values"] = tuple(self.all_medicine_names)
            return
        self.sale_combo["values"] = tuple(
            [name for name in self.all_medicine_names if name.lower().startswith(query)]
        )

    def filter_patients_for_sale(self, event=None):
        query = self.patient_combo.get().strip().lower()
        self.patient_combo["values"] = tuple([name for name in self.all_patient_names if query in name.lower()])

    def refresh_sales_tab(self):
        if not hasattr(self, "sales_tree") or not self.sales_tree.winfo_exists():
            return

        for row in self.sales_tree.get_children():
            self.sales_tree.delete(row)

        self.cursor.execute(
            """
            SELECT
                s.id,
                p.name,
                s.sale_date,
                s.total_amount,
                GROUP_CONCAT(CONCAT(m.name, ':', COALESCE(si.prescription, '-')) SEPARATOR ' ; ') AS prescription_text
            FROM sales s
            LEFT JOIN patients p ON s.patient_id = p.id
            LEFT JOIN sale_items si ON si.sale_id = s.id
            LEFT JOIN medicines m ON si.medicine_id = m.id
            GROUP BY s.id, p.name, s.sale_date, s.total_amount
            ORDER BY s.id DESC
            """
        )
        rows = self.cursor.fetchall()

        for row in rows:
            sale_id = self._row_value(row, "id", 0)
            patient_name = self._row_value(row, "name", 1)
            sale_date = self._row_value(row, "sale_date", 2)
            total = self._row_value(row, "total_amount", 3)
            prescription_text = self._row_value(row, "prescription_text", 4, "-") or "-"
            self.sales_tree.insert("", "end", values=(sale_id, patient_name, sale_date, prescription_text, total))
