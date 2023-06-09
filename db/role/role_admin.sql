-- CREATE ADMIN ROLE:
CREATE ROLE [admin];
-- VIEW FOR ADMIN
GRANT SELECT ON v_user_info TO [admin];
-- Store Procedure: 
GRANT EXECUTE ON sp_post_course TO [admin];
GRANT EXECUTE ON sp_delete_course TO [admin];
GRANT EXECUTE ON sp_update_course TO [admin];
GRANT EXECUTE ON sp_update_user_authorization TO [admin];
GRANT EXECUTE ON sp_delete_user TO [admin];
GRANT EXECUTE ON sp_role_to_user TO [admin];


-- SCALAR VALUED FUNCTIONS:
GRANT EXECUTE ON func_check_level_and_category_exists TO [admin];

