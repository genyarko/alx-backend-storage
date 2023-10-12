-- Create a trigger to reset 'valid_email' when 'email' is changed
DELIMITER //
CREATE TRIGGER reset_valid_email_on_email_change
BEFORE UPDATE ON your_table_name -- Replace 'your_table_name' with the actual table name
FOR EACH ROW
BEGIN
    IF NEW.email <> OLD.email THEN
        SET NEW.valid_email = 0;
    END IF;
END;
//
DELIMITER ;
