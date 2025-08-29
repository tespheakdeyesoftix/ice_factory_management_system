SQL="""create function `fn_get_payment_status`(sale_amount FLOAT,
    payment_amount FLOAT
) RETURNS varchar(50) 
    DETERMINISTIC
BEGIN
    IF payment_amount = 0 THEN
        RETURN 'Unpaid';
    ELSEIF sale_amount - payment_amount > 0 THEN
        RETURN 'Partially Paid';
    ELSE
        RETURN 'Paid';
    END IF;
END;
"""