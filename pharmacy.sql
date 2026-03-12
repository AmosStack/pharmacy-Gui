USE pharmacy;

DROP TABLE IF EXISTS sale_items;
DROP TABLE IF EXISTS stock_entries;
DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS medicines;
DROP TABLE IF EXISTS patients;
DROP TABLE IF EXISTS users;

CREATE TABLE medicines (
  id INT IDENTITY(1,1) NOT NULL,
  name VARCHAR(255) NOT NULL,
  type VARCHAR(50) NOT NULL CONSTRAINT DF_medicines_type DEFAULT 'Tablet',
  expiry_date DATE DEFAULT NULL,
  price DECIMAL(10, 2) DEFAULT NULL,
  quantity INT DEFAULT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE patients (
  id INT IDENTITY(1,1) NOT NULL,
  name VARCHAR(255) NOT NULL,
  age INT DEFAULT NULL,
  medical_history TEXT,
  PRIMARY KEY (id)
);

CREATE TABLE users (
  id INT IDENTITY(1,1) NOT NULL,
  username VARCHAR(100) NOT NULL,
  password VARCHAR(255) NOT NULL,
  [role] VARCHAR(20) NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT UQ_users_username UNIQUE (username)
);

CREATE TABLE sales (
  id INT IDENTITY(1,1) NOT NULL,
  sale_date DATE DEFAULT NULL,
  total_amount DECIMAL(10, 2) DEFAULT NULL,
  patient_id INT DEFAULT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_sales_patient FOREIGN KEY (patient_id) REFERENCES patients (id)
);

CREATE TABLE sale_items (
  id INT IDENTITY(1,1) NOT NULL,
  sale_id INT DEFAULT NULL,
  medicine_id INT DEFAULT NULL,
  quantity INT DEFAULT NULL,
  subtotal DECIMAL(10, 2) DEFAULT NULL,
  prescription VARCHAR(255) DEFAULT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_sale_items_sale FOREIGN KEY (sale_id) REFERENCES sales (id),
  CONSTRAINT fk_sale_items_medicine FOREIGN KEY (medicine_id) REFERENCES medicines (id)
);

CREATE TABLE stock_entries (
  id INT IDENTITY(1,1) NOT NULL,
  medicine_id INT DEFAULT NULL,
  quantity_added INT DEFAULT NULL,
  entry_date DATE DEFAULT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_stock_entries_medicine FOREIGN KEY (medicine_id) REFERENCES medicines (id)
);

CREATE INDEX idx_sales_patient_id ON sales (patient_id);
CREATE INDEX idx_sale_items_sale_id ON sale_items (sale_id);
CREATE INDEX idx_sale_items_medicine_id ON sale_items (medicine_id);
CREATE INDEX idx_stock_entries_medicine_id ON stock_entries (medicine_id);

MERGE users AS target
USING (
  VALUES
    ('admin', 'admin123', 'manager'),
    ('staff1', '1234', 'staff')
) AS source (username, password, role)
ON target.username = source.username
WHEN MATCHED THEN
  UPDATE SET
    target.password = source.password,
    target.[role] = source.role
WHEN NOT MATCHED BY TARGET THEN
  INSERT (username, password, [role])
  VALUES (source.username, source.password, source.role);