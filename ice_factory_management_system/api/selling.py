import frappe 
@frappe.whitelist()
def get_dashboard_data(outlet, date):
    # outlet, date
    sql = """select 
            count(*) as total_order, 
            sum(total_sale_quantity) as total_quantity, 
            sum(total_amount) as total_amount 
        from `tabSale` 
    where 
    sale_status = 'Closed' and 
    sale_date = %(date)s and 
    outlet = %(outlet)s 
    """
    data = frappe.db.sql(sql,{"outlet":outlet, "date":date},as_dict = 1)
 
    if data: 
        return data[0]
    
    return {
        "total_order":0,
        "total_quantity":0,
        "total_amount": 0
    }

@frappe.whitelist()
def get_total_daily_sale_product_summary(outlet, date):
    # outlet, date
    sql = """select 
            sp.product_code,
            sp.product_name,
            sum(sp.quantity) as quantity, 
            sum(sp.free_quantity) as free_quantity, 
            sum(sp.return_quantity) as return_quantity, 
            sum(coalesce(sp.total_sale_quantity,0)) as sale_quantity, 
            sum(sp.total_amount) as total_amount 
        from `tabSale Products` sp
        inner join `tabSale` s on s.name = sp.parent

    where 
        s.sale_status = 'Closed' and 
        s.sale_date = %(date)s and 
        s.outlet = %(outlet)s 
    group by
        sp.product_code,
        sp.product_name
        
    """
    data = frappe.db.sql(sql,{"outlet":outlet, "date":date},as_dict = 1)
    return data


