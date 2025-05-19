#  E-Commerce API

A simple FastAPI-based backend service for managing an e-commerce system. It handles products, inventory, and sales.

---

## 🚀 Features

- Manage product catalog
- Track inventory levels
- Record and query sales
- RESTful API Swagger docs

---

## 🧰 Tech Stack

- Python 3.11
- FastAPI
- Uvicorn
- MYSQL
- Pydantic

---

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/ecomm-api.git
cd ecomm-api
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
uvicorn ecomm.main:app --reload
```

### 4. Run the Demo Data Script

```bash
This will populate Demo Data
python db/demo_data.py
```

### 5. Run with Docker

```bash
docker build -t ecomm-api .
docker run -p 8000:8000 ecomm-api

Running from docker will auto insert some dummy data
```

---

## 📡 API Endpoints

Interactive API documentation is available at:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

| Method | Endpoint                                                                                                                          | Description                                                                                 |
|--------|-----------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| GET    | `/`                                                                                                                               | Show that tha APi is working and is up                                                      |
| GET    | `/products`                                                                                                                       | List all products                                                                           |
| POST   | `/products`                                                                                                                       | Create a new product                                                                        |
| GET    | `/inventory`                                                                                                                      | View inventory levels                                                                       |
| PUT    | `/inventory/update`                                                                                                               | Update inventory for a product along with last updated to track changes                     |
| PUT    | `/inventory/lowStock`                                                                                                             | Get the Alert of Low Stcok if stock is less than LOW_STOCK_THRESHOLD which is by default 10 |
| GET    | `/sales`                                                                                                                          | List all sales records                                                                      |
| GET    | `/sales/filter?start_date=2024-05-01&end_date=2024-05-02`                                                                         | List a sale in specific Date Range                                                          |
| GET    | `/sales/filter?start_date=2024-05-02&end_date=2024-05-0&category=Electronics`                                                     | List a sale in specific Date Range and Category                                             |
| GET    | `/sales/filter?start_date=2024-05-02&end_date=2024-05-0&product_id=2`                                                             | List a sale in specific Date Range and Product                                              |
| GET    | `/sales/filter?start_date=2024-05-02&end_date=2024-05-0&product_id=2&category=Electronics`                                        | List a sale in specific Date Range and Product and Category                                 |
| GET    | `/sales/compare?start_date_1=2024-05-01&end_date_1=2024-05-01&start_date_2=2024-05-02&end_date_2=2024-05-02'`                     | Compare a Revenue in specific Date Range                                                    |
| GET    | `sales/compare?start_date_1=2024-05-01&end_date_1=2024-05-01&start_date_2=2024-05-02&end_date_2=2024-05-02&category=Electronics'` | Compare a Revenue in specific Date Range and Category                                       |
| GET    | `/revenue`                                                                                                                        | List all revenue records                                                                    |
| GET    | `/revenue?period=weekly`                                                                                                          | List in specific Range (Weekly,Monthly,Yearly,Daily)                                        |

---

## 🧱 Database Schema

This app uses mysql-connector-python.

### 🛒 `Product` Table

| Field       | Type     | Description                |
|-------------|----------|----------------------------|
| id          | Integer  | Primary key                |
| name        | String   | Name of the product        |
| category    | String   | Category of Product        |
| price       | Float    | Price per unit             |
---

### 📦 `Inventory` Table

| Field       | Type     | Description                              |
|-------------|----------|------------------------------------------|
| id          | Integer  | Primary key                              |
| product_id  | Integer  | Foreign key to Product.id                |
| quantity    | Integer  | Available stock units                    |
| last_updated| TIMESTAMP| Track changes when quantitity is updated |

**Relationship**: One-to-one with `Product`. Each product has a corresponding inventory record.

---

### 💰 `Sales` Table

| Field       | Type     | Description                      |
|-------------|----------|----------------------------------|
| id          | Integer  | Primary key                      |
| product_id  | Integer  | Foreign key to Product.id        |
|quantity_sold| Integer  | Number of units sold             |
| sale_date   | DateTime | Timestamp of the sale            |

**Relationship**: Many-to-one with `Product`. Each sale entry links to a product.

**Indexing**: Added indexing on 
sales.product_id: For the JOIN
and sales.sale_date: For potential GROUP BY and ORDER BY optimization.
