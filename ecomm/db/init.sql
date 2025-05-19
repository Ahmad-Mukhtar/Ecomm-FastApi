-- Create tables
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS inventory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    quantity_sold INT NOT NULL,
    sale_date DATE NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

CREATE INDEX idx_sales_product_id ON sales (product_id);
CREATE INDEX idx_sales_sale_date ON sales (sale_date);


-- Insert sample data
INSERT INTO products (name, category, price) VALUES
('iPhone 13', 'Electronics', 999.99),
('Samsung TV', 'Electronics', 599.99),
('Coffee Maker', 'Appliances', 89.99);

INSERT INTO inventory (product_id, quantity) VALUES
(1, 50),
(2, 75),
(3, 100);

INSERT INTO sales (product_id, quantity_sold, sale_date) VALUES
(1, 2, '2024-05-01'),
(2, 1, '2024-05-02'),
(3, 3, '2024-05-03');