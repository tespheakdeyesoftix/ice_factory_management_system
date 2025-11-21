import frappe
from frappe.utils import getdate, today,add_to_date


@frappe.whitelist()
def get_customer_dashboard_data(customer="", start_date = None, end_date=None, outlet=""):
 

    if not start_date:
        start_date =  getdate(today()).replace(day=1)
    if not end_date:
        end_date = today()

    return {
        "account_recivable": get_account_receivable_data(outlet=outlet,start_date=start_date,end_date=end_date,customer=customer ),
        "ar_aging":get_customer_ar_aging(customer=customer, outlet=outlet)
    }

@frappe.whitelist()
def get_account_receivable_data( customer = "", start_date= None, end_date=None, outlet=""):
    # opening 
    sql  = """select 
                    sum(debit_amount-credit_amount) as total 
                from `tabGL Entry` gl join `tabChart of Account` acc on acc.name = gl.account 
                where 
                    gl.posting_date < %(start_date)s and 
                    acc.account_type='Receivable' and (%(outlet)s = '' or gl.outlet = %(outlet)s) 
                    and party_type='Customer' and 
                    party=%(customer)s
                """ 
    
    data = frappe.db.sql(sql,{"outlet":outlet,"start_date":start_date,"customer":customer},as_dict=1)

    return_data ={
        "opening" : data[0].get("total") or 0
    }
    # current debit and credit
    sql  = """select 
                sum(if(transaction_type='Receivable',debit_amount,0)) as debit_amount,
                sum(if(transaction_type='Payment',credit_amount,0)) as payment_amount,
                sum(if(transaction_type='Write Off',credit_amount,0)) as write_off_amount
            from `tabGL Entry` gl join `tabChart of Account` acc on acc.name = gl.account 
            where 
                gl.posting_date between %(start_date)s and %(end_date)s and 
                acc.account_type='Receivable' and (%(outlet)s = '' or gl.outlet = %(outlet)s) 
                and party_type='Customer' and 
                party=%(customer)s""" 
    
    data = frappe.db.sql(sql,{"outlet":outlet,"start_date":start_date,"end_date":end_date,"customer":customer},as_dict=1)

    return_data["debit_amount"] = data[0].get("debit_amount") or 0
    return_data["payment_amount"] = data[0].get("payment_amount") or 0
    return_data["write_off_amount"] = data[0].get("write_off_amount") or 0
    return_data["balance"] = return_data.get("opening") + return_data.get("debit_amount")  - ( return_data.get("payment_amount") + return_data.get("payment_amount"))

 
    return return_data

@frappe.whitelist()
def get_customer_ar_aging(customer="",outlet=""):
    sql ="""
        SELECT 
            period_name,
            SUM(balance) AS amount
        FROM (
            SELECT
                CASE
                    WHEN age_days <= 0 THEN 'current'
                    WHEN age_days BETWEEN 1 AND 7 THEN 'day_7'
                    WHEN age_days BETWEEN 8 AND 15 THEN 'day_15'
                    WHEN age_days BETWEEN 16 AND 30 THEN 'day_30'
                    WHEN age_days BETWEEN 31 AND 60 THEN 'day_60'
                    WHEN age_days BETWEEN 61 AND 90 THEN 'day_90'
                    WHEN age_days BETWEEN 91 AND 120 THEN 'day_120'
                    WHEN age_days > 120 THEN 'day_120_plus'
                END AS period_name,
                balance
            FROM (
                SELECT
                    COALESCE(gl.against_voucher_no, gl.voucher_no) AS voucher_number,
                    MIN(gl.posting_date) AS posting_date,
                        SUM(gl.debit_amount - gl.credit_amount) AS balance,
                        DATEDIFF(CURDATE(), MIN(gl.posting_date)) AS age_days
                    FROM `tabGL Entry` gl
                    JOIN `tabChart of Account` acc ON acc.name = gl.account
                    WHERE 
                        gl.party_type = 'Customer'
                        AND acc.account_type = 'Receivable' and 
                        gl.party = %(customer)s and 
                        (%(outlet)s = '' or gl.outlet = %(outlet)s)
                    
                    GROUP BY voucher_number
                    HAVING balance <> 0
                ) x
            ) y
            GROUP BY period_name
    """
    data = frappe.db.sql(sql,{"customer":customer,"outlet":outlet},as_dict=1)
    period_range = [
        {'label': 'Current', 'fieldname': 'current', 'amount': 0, 'percent': 0, 'color': '#4caf50'},
        {'label': '7 Days', 'fieldname': 'day_7', 'amount': 0, 'percent': 0, 'color': '#8bc34a'},
        {'label': '15 Days', 'fieldname': 'day_15', 'amount': 0, 'percent': 0, 'color': '#ffeb3b'},
        {'label': '30 Days', 'fieldname': 'day_30', 'amount': 0, 'percent': 0, 'color': '#ffc107'},
        {'label': '60 Days', 'fieldname': 'day_60', 'amount': 0, 'percent': 0, 'color': '#ff9800'},
        {'label': '90 Days', 'fieldname': 'day_90', 'amount': 0, 'percent': 0, 'color': '#ff5722'},
        {'label': '120 Days', 'fieldname': 'day_120', 'amount': 0, 'percent': 0, 'color': '#f44336'},
        {'label': '120+ Days', 'fieldname': 'day_120_plus', 'amount': 0, 'percent': 0, 'color': '#b71c1c'}
    ]

    total = sum([d.get("amount") for d in data])
    for d in data:
        row =  next((x for x in period_range if x.get("fieldname") == d.get("period_name")), None)
        
        if row:
            row["amount"] = d.get("amount")
            row["percent"] = d.get("amount") / (max(total,1))
    return period_range



@frappe.whitelist()
def get_sale_vs_payment_chart_data(series_type="MTD", customer="",outlet=""):

    start_date = None
    end_date= None
    data = []
    if series_type == "MTD":
       
        start_date =  getdate(today()).replace(day=1)
        end_date = add_to_date(start_date, months=1)
        end_date = add_to_date(end_date, days=-1)
        sql = """
                with a as (
                    select date from `tabDates` where date between %(start_date)s and %(end_date)s
                ),b as (
                    select 
                        s.posting_date,
                        sum(s.total_amount) as amount 
                    from `tabSale` s
                    where 
                        s.sale_status = 'Closed'  and 
                        (%(outlet)s = '' or s.outlet=%(outlet)s) and 
                        (%(customer)s = '' or s.customer = %(customer)s) and 
                        s.posting_date between %(start_date)s and %(end_date)s

                    group by
                        s.posting_date
                ),
                c as (
                    select 
                        s.posting_date,
                        sum(s.paid_amount) as payment_amount ,
                        sum(s.write_off_amount) as write_off_amount 
                    from `tabSale Payment Invoices` s
                    where 
                        s.docstatus = 1 and  
                        (%(outlet)s = '' or s.outlet=%(outlet)s) and 
                        (%(customer)s = '' or s.customer = %(customer)s) and 
                        s.posting_date between %(start_date)s and %(end_date)s

                    group by
                        s.posting_date
                )
                select 
                    day(a.date) as date,
                    coalesce(b.amount,0) as sale_amount,
                    coalesce(c.payment_amount,0) as payment_amount,
                    coalesce(c.write_off_amount,0) as write_off_amount
                from a 
                left join b on b.posting_date = a.date
                left join c on b.posting_date = a.date
                order by date
                """
        data =  frappe.db.sql(sql,{"start_date":start_date,"end_date":end_date,"outlet":outlet,"customer":customer},as_dict = 1)
        
        
    
    else:
        start_date =  getdate(today()).replace(day=1,month=1)
        end_date = add_to_date(start_date, years=1)
        end_date = add_to_date(end_date, days=-1)
        sql = """
                with a as (
                    select DATE_FORMAT(date, '%%b') AS month_text, month(date) as `month`, year(date) as `year` from `tabDates` where date between %(start_date)s and %(end_date)s group by `month`,`year`
                ),b as (
                    select 
                        month(s.posting_date) as `month`,
                        year(s.posting_date) as `year`,
                        sum(s.total_amount) as amount 
                    from `tabSale` s
                    where 
                        s.sale_status = 'Closed'  and 
                        (%(outlet)s = '' or s.outlet=%(outlet)s) and 
                        (%(customer)s = '' or s.customer = %(customer)s) and 
                        s.posting_date between %(start_date)s and %(end_date)s

                    group by
                        `month`,
                        `year`
                ),
                c as (
                    select 
                        month(s.posting_date) as month,
                        year(s.posting_date) as year,
                        sum(s.paid_amount) as payment_amount ,
                        sum(s.write_off_amount) as write_off_amount 
                    from `tabSale Payment Invoices` s
                    where 
                        s.docstatus = 1 and  
                        (%(outlet)s = '' or s.outlet=%(outlet)s) and 
                        (%(customer)s = '' or s.customer = %(customer)s) and 
                        s.posting_date between %(start_date)s and %(end_date)s

                    group by
                        `month`,
                        `year`
                )
                select 
                    a.month_text,
                    coalesce(b.amount,0) as sale_amount,
                    coalesce(c.payment_amount,0) as payment_amount,
                    coalesce(c.write_off_amount,0) as write_off_amount
                from a 
                left join b on b.`month` = a.`month` and b.`year` = a.`year`
                left join c on c.`month` = a.`month` and c.`year` = a.`year`
                 
                """
        data =  frappe.db.sql(sql,{"start_date":start_date,"end_date":end_date,"outlet":outlet,"customer":customer},as_dict = 1)
        
    
    
    return data

@frappe.whitelist()
def get_total_order_chart_data(series_type="MTD", customer="",outlet=""):
    start_date = None
    end_date= None
    data = []
    if series_type == "MTD":
        start_date =  getdate(today()).replace(day=1)
        end_date = add_to_date(start_date, months=1)
        end_date = add_to_date(end_date, days=-1)
        sql = """
                with a as (
                    select date from `tabDates` where date between %(start_date)s and %(end_date)s
                ),b as (
                    select 
                        s.posting_date,
                        count(*) as total_order
                    from `tabSale` s
                    where 
                        s.sale_status = 'Closed'  and 
                        (%(outlet)s = '' or s.outlet=%(outlet)s) and 
                        (%(customer)s = '' or s.customer = %(customer)s) and 
                        s.posting_date between %(start_date)s and %(end_date)s

                    group by
                        s.posting_date
                )
                select 
                    day(a.date) as date,
                    coalesce(b.total_order,0) as total_order
                from a 
                left join b on b.posting_date = a.date
                 
                """
        data =  frappe.db.sql(sql,{"start_date":start_date,"end_date":end_date,"outlet":outlet,"customer":customer},as_dict = 1)
        
        
    
    else:
        start_date =  getdate(today()).replace(day=1,month=1)
        end_date = add_to_date(start_date, years=1)
        end_date = add_to_date(end_date, days=-1)
        sql = """
                with a as (
                    select DATE_FORMAT(date, '%%b') AS month_text, month(date) as `month`, year(date) as `year` from `tabDates` where date between %(start_date)s and %(end_date)s group by `month`,`year`
                ),b as (
                    select 
                        month(s.posting_date) as `month`,
                        year(s.posting_date) as `year`,
                        count(*) as total_order
                    from `tabSale` s
                    where 
                        s.sale_status = 'Closed'  and 
                        (%(outlet)s = '' or s.outlet=%(outlet)s) and 
                        (%(customer)s = '' or s.customer = %(customer)s) and 
                        s.posting_date between %(start_date)s and %(end_date)s

                    group by
                        `month`,
                        `year`
                )
                select 
                    a.month_text,
                    coalesce(b.total_order,0) as total_order
                    
                from a 
                left join b on b.`month` = a.`month` and b.`year` = a.`year`
                 
                 
                """
        data =  frappe.db.sql(sql,{"start_date":start_date,"end_date":end_date,"outlet":outlet,"customer":customer},as_dict = 1)
        
    
    
    return data

@frappe.whitelist()
def get_total_order_quantity_chart_data(series_type="MTD", customer="",outlet=""):
    outlets = []
    if outlet:
        outlets = [outlet]
    else:
        outlets = frappe.get_list("Outlet",pluck="name")
        
    start_date = None
    end_date= None
    data = []
    outlet_fields = ", ".join([f"0 as `{f}`" for f in outlets])
    if series_type == "MTD":
        start_date =  getdate(today()).replace(day=1)
        end_date = add_to_date(start_date, months=1)
        end_date = add_to_date(end_date, days=-1)
        
        sql = """
                    select day(date) as date,{0} from `tabDates` where date between %(start_date)s and %(end_date)s 
                
        """.format(outlet_fields)
        data =  frappe.db.sql(sql,{"start_date":start_date,"end_date":end_date},as_dict = 1)

        # quantity data
        sql = """
            select 
                s.outlet,
                day(s.posting_date) as date,
                sum(s.total_sale_quantity) as quantity 
            from  `tabSale`  s
            where
                s.posting_date between %(start_date)s and %(end_date)s  and 
                s.outlet in %(outlets)s and 
                (%(customer)s = '' or  s.customer = %(customer)s )
            group by 
                s.outlet,
                s.posting_date
        """
        quantity_data = frappe.db.sql(sql,{"start_date":start_date,"end_date":end_date,"customer":customer,"outlets":outlets},as_dict =1)
        for q in quantity_data:
            row = next((x for x in data if  x.get("date")  ==  q.get("date")), None)
            if row:
                row[q.get("outlet")] = q.get("quantity")
        
       
        
    
    else:
        start_date =  getdate(today()).replace(day=1,month=1)
        end_date = add_to_date(start_date, years=1)
        end_date = add_to_date(end_date, days=-1)
        sql = """
                    select DATE_FORMAT(date, '%%b') AS date, month(date) as `month`,year(date) as `year`,{0} from `tabDates` 
                    where date between %(start_date)s and %(end_date)s  
                    group by
                        `month`,
                        `year`
                
        """.format(outlet_fields)
        data =  frappe.db.sql(sql,{"start_date":start_date,"end_date":end_date},as_dict = 1)
        # quantity data
        sql = """
            select 
                s.outlet,
                month(s.posting_date) as `month`,
                year(s.posting_date) as `year`,
                sum(s.total_sale_quantity) as quantity 
            from  `tabSale` s
            where
                s.posting_date between %(start_date)s and %(end_date)s  and 
                s.outlet in %(outlets)s and 
                (%(customer)s = '' or  s.customer = %(customer)s )
            group by 
                s.outlet,
                `month`,
                `year`
        """
        quantity_data = frappe.db.sql(sql,{"start_date":start_date,"end_date":end_date,"customer":customer,"outlets":outlets},as_dict =1)
        for q in quantity_data:
            row = next((x for x in data if  x.get("month")  ==  q.get("month") and x.get("year")  ==  q.get("year")), None)
            if row:
                row[q.get("outlet")] = q.get("quantity")
    
    return {"chart_data":data,"chart_data_fields":outlets}



    
@frappe.whitelist()
def get_revenue_summary(start_date=None,end_date=None, customer="",outlet="",group_by="product_category"):
    outlets = []
    if outlet:
        outlets = [outlet]
    else:
        outlets = frappe.get_list("Outlet",pluck="name")
        
    
    data = []
    
    if not start_date:
        start_date =  getdate(today()).replace(day=1)
    if not end_date:
        end_date = today()
    sql = """
        select 
            sp.{0} as label,
            sum(sp.total_amount) as value 
        from `tabSale Products` sp join `tabSale` s on s.name = sp.parent
        where
            s.sale_status = 'Closed' and 
            s.outlet in %(outlets)s and
            (%(customer)s = '' or s.customer = %(customer)s ) and  
            s.posting_date between %(start_date)s and %(end_date)s
        group by
         label
        """.format(
            group_by
        )
    data = frappe.db.sql (sql,{"customer":customer,"outlets":outlets,"start_date":start_date,"end_date":end_date},as_dict = 1)
    return data