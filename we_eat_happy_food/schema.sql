CREATE TABLE IF NOT EXISTS 'user'(
    'username' TEXT NOT NULL,
    'password_hash' TEXT NOT NULL
);

-- Insert test user --

INSERT INTO user(username, password_hash) VALUES(
    'melon','2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'
);

--Create category table separately to avoid typo category mistake --
CREATE TABLE IF NOT EXISTS 'category'(
    'name' TEXT PRIMARY KEY

);

CREATE TABLE IF NOT EXISTS 'post'(
    'url_slug' TEXT PRIMARY KEY,
    'title' TEXT NOT NULL,
    'author' TEXT NOT NULL,
    'time_created' DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    'body' TEXT NOT NULL
);

-- many to many relationship in category --
CREATE TABLE IF NOT EXISTS 'post_category'(
    'category_name' TEXT NOT NULL,
    'url_slug' TEXT NOT NULL,
    FOREIGN KEY (category_name) REFERENCES category(name),
    FOREIGN KEY (url_slug) REFERENCES post(url_slug)
);

INSERT INTO category(name) VALUES
    ('Recipes'),
    ('Breakfast'),
    ('Lunch'),
    ('Dinner'),
    ('Salad'),
    ('Snacks');


INSERT INTO post (title,url_slug,author,time_created,body) VALUES (
    'A random post 2',
    'a-random-post-2',
    'Melon',
    datetime('now'),
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
);

INSERT INTO post_category (category_name, url_slug) VALUES
    ('Snacks', 'a-random-post-2'),
    ('Recipes', 'a-random-post-2');

