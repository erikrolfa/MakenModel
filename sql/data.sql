PRAGMA foreign_keys = ON;

INSERT INTO users(username, password, email, profile_pic_filename)
VALUES ('test_user', 'sha512$1ae6e8a6c6224f2d8cf360e5fc8bc3af$f9d6ea7ebd2efc5f4093ffc2014a25daa7738941345849bde566296cb6f975a2b78da457744a54031d2ec9670ba798edc3e9c2b18518cfdb333e70d77d0c0aef', 'test@test.com', 'test_profile_pic')