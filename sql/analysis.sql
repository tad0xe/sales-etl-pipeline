SELECT COUNT(*) AS total_orders
FROM orders;
SELECT ROUND(SUM(total_price), 2) AS total_sales
FROM orders;
SELECT
    category,
    ROUND(SUM(total_price), 2) AS total_sales
FROM orders
GROUP BY category
ORDER BY total_sales DESC;
SELECT
    product_name,
    SUM(quantity) AS total_quantity_sold,
    ROUND(SUM(total_price), 2) AS revenue
FROM orders
GROUP BY product_name
ORDER BY revenue DESC
LIMIT 5;
SELECT
    country,
    COUNT(*) AS number_of_orders,
    ROUND(SUM(total_price), 2) AS revenue
FROM orders
GROUP BY country
ORDER BY revenue DESC;
SELECT
    order_status,
    COUNT(*) AS total_orders
FROM orders
GROUP BY order_status
ORDER BY total_orders DESC;