SQL="""CREATE PROCEDURE get_monthly_data(
  IN p_posting_date DATE,p_outlet NVARCHAR(100)
)
BEGIN
with sales as(SELECT 
SUM(total_amount) total_sale_amount,
coalesce(outlet,'None') outlet,
COUNT(NAME) sales,
sum(total_quantity) total_quantity,
sum(total_free) total_free,
sum(total_quantity_return) total_quantity_return,
sum(total_sale_quantity) total_sale_quantity,
cast(sum(total_amount)/sum(total_sale_quantity) AS DECIMAL(16,2)) average_price
FROM `tabSale` 
WHERE month(posting_date) = MONTH(p_posting_date) AND YEAR(posting_date) = YEAR(p_posting_date) AND 
`status` <> 'Deleted' AND sale_status = 'Closed'
GROUP BY coalesce(outlet,'None')
)
,deleted_sales AS(
SELECT SUM(sales) sales,outlet from(
SELECT 0 'sales',NAME outlet FROM `tabOutlet`
UNION all
SELECT 
COUNT(NAME) sales,
coalesce(outlet,'None') outlet
FROM `tabSale` 
WHERE month(posting_date) = MONTH(p_posting_date) AND YEAR(posting_date) = YEAR(p_posting_date) AND 
`status` =  'Deleted' AND sale_status = 'Deleted'
GROUP BY coalesce(outlet,'None')) a GROUP BY outlet
)
,payments AS(
SELECT 
sum(total_paid) total_paid,
sum(write_off_amount) write_off_amount,
COALESCE(a.outlet,'None') outlet
FROM `tabSale Payment` a
INNER JOIN `tabSale` b ON b.name = a.sale
WHERE MONTH(a.posting_date) = MONTH(p_posting_date) AND YEAR(a.posting_date) = YEAR(p_posting_date) AND b.`status` <> 'Deleted' AND sale_status = 'Closed'
GROUP BY coalesce(outlet,'None')
)
,bank_transfer AS(
SELECT SUM(amount) amount,outlet from(
SELECT 0 'amount',NAME outlet FROM `tabOutlet`
UNION all
SELECT 
coalesce(sum(amount),0) amount,
coalesce(outlet,'None') outlet
FROM `tabBank Transfer`
WHERE month(posting_date) = MONTH(p_posting_date) AND YEAR(posting_date) = YEAR(p_posting_date) AND docstatus=1
GROUP BY coalesce(outlet,'None')) transfer GROUP BY outlet
)
,current_receivables AS(
SELECT 
SUM(debit_amount - credit_amount) AS receivable_balance,
coalesce(outlet,'None') outlet
FROM `tabGL Entry` 
WHERE is_cancelled = 0 
AND `account` IN (SELECT name FROM `tabChart of Account` WHERE account_type = 'Receivable') AND
month(posting_date) = MONTH(p_posting_date) AND YEAR(posting_date) = YEAR(p_posting_date)
GROUP BY coalesce(outlet,'None')
)
,receivables AS(
SELECT 
SUM(debit_amount - credit_amount) AS receivable_balance,
coalesce(outlet,'None') outlet
FROM `tabGL Entry` 
WHERE is_cancelled = 0 
AND `account` IN (SELECT name FROM `tabChart of Account` WHERE account_type = 'Receivable')
GROUP BY coalesce(outlet,'None')
)
,tube_ice AS(
SELECT 
coalesce(SUM(total_produce_quantity),0) total_produce_quantity,
coalesce(SUM(total_produce_drop),0) total_produce_drop,
coalesce(SUM(total_infected_quantity),0) total_infected_quantity 
FROM `tabTube Ice Produce` 
WHERE docstatus = 1 and month(posting_date) = MONTH(p_posting_date) AND YEAR(posting_date) = YEAR(p_posting_date)
)
,block_ice AS(
SELECT 
coalesce(SUM(total_produce_quantity),0) total_produce_quantity 
FROM `tabBlock Ice Produce` 
WHERE docstatus = 1 and month(posting_date) = MONTH(p_posting_date) AND YEAR(posting_date) = YEAR(p_posting_date)
)
SELECT * FROM(
SELECT 'total_paid' label,outlet,total_paid `value` FROM payments
UNION ALL
SELECT 'write_off_amount' label,outlet,write_off_amount `value` FROM payments
UNION ALL
SELECT 'total_produce_quantity' label,'Tube Ice' outlet,total_produce_quantity `value` FROM tube_ice
UNION ALL
SELECT 'total_produce_quantity' label,'Block Ice' outlet,total_produce_quantity `value` FROM block_ice
UNION ALL
SELECT 'total_produce_drop' label,'Tube Ice' outlet,total_produce_drop `value` FROM tube_ice
UNION ALL
SELECT 'total_infected_quantity' label,'Tube Ice' outlet,total_infected_quantity `value` FROM tube_ice
UNION ALL
SELECT 'sales' label,outlet,sales `value` FROM sales
UNION ALL
SELECT 'total_sale_amount' label,outlet,total_sale_amount `value` FROM sales
UNION all
SELECT 'bank_transfer' label,outlet,amount `value` FROM bank_transfer
UNION ALL
SELECT 'deleted_sales' label,outlet,sales `value` FROM deleted_sales
UNION ALL
SELECT 'total_quantity' label,outlet,total_quantity `value` FROM sales
UNION ALL
SELECT 'total_free' label,outlet,total_free `value` FROM sales
UNION ALL
SELECT 'total_quantity_return' label,outlet,total_quantity_return `value` FROM sales
UNION ALL
SELECT 'total_sale_quantity' label,outlet,total_sale_quantity `value` FROM sales
UNION ALL
SELECT 'average_price' label,outlet,average_price `value` FROM sales
UNION ALL
SELECT 'current_receivable_balance' label,outlet,receivable_balance `value` FROM current_receivables
UNION ALL
SELECT 'receivable_balance' label,outlet,receivable_balance `value` FROM receivables
) as working_data WHERE outlet = case when p_outlet = 'All' then outlet ELSE p_outlet end;
END"""