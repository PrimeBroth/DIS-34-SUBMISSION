import os
import sys

paths = {
    'root': os.path.dirname(os.path.abspath(__file__)),
    'src': os.path.join(os.path.dirname(os.path.abspath(__file__)),'src'),
    'tmp': os.path.join(os.path.dirname(os.path.abspath(__file__)),'tmp'),
    'static': os.path.join(os.path.dirname(os.path.abspath(__file__)),'src', 'static'),
    'dikumon': os.path.join(os.path.dirname(os.path.abspath(__file__)),'src', 'static', 'dikumon'),   
}

sql = f'''
drop table if exists dikumon cascade;
drop table if exists users cascade;
drop table if exists reviews cascade;

CREATE TABLE IF NOT EXISTS users(
    username char(20) NOT NULL,
    password char(20) NOT NULL,
    CONSTRAINT user_pk PRIMARY KEY (username));

create table dikumon(
number int,
name varchar(256) primary key,
type1 varchar(256),
type2 varchar(256),
total int,
hp int,
attack int,
defense int,
sp_attack int,
sp_defense int,
speed int,
generation int,
legendary boolean
);

\COPY dikumon FROM '{os.path.join(paths['tmp'], 'Pokemon.csv')}' DELIMITER ',' CSV HEADER;

ALTER TABLE dikumon ADD COLUMN username char(20);
ALTER TABLE dikumon ADD FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE;

create table reviews(
    rid int primary key,
    username char(20),
    name varchar(256),
    rating int,
    review varchar(256),
    foreign key (username) references users(username) ON DELETE CASCADE,
    foreign key (name) references dikumon(name) ON DELETE CASCADE
);
'''

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print('Usage: python init_project.py <dbname> <user> <host> <password>')
        sys.exit(1)
    dbname = sys.argv[1]
    user = sys.argv[2]
    host = sys.argv[3]
    password = sys.argv[4]

    # write paths to csv
    with open(os.path.join(paths['src'],'paths.csv'), 'w') as f:
        for key, value in paths.items():
            f.write(f'{key},{value}\n')

    # assert file was created
    assert os.path.exists(os.path.join(paths['src'],'paths.csv')), 'File not created'

    # write to file
    with open(os.path.join(paths['root'],'init_db_test.sql'), 'w') as f:
        f.write(sql)
    
    # assert file was created
    assert os.path.exists(os.path.join(paths['root'],'init_db_test.sql')), 'File not created'

    # run sql with psql
    os.system(f'psql -h {host} -U {user} -d {dbname} -f {os.path.join(paths["root"], "init_db_test.sql")}')

    # run src/app.py
    os.system(f'python {os.path.join(paths["src"], "app.py")} {dbname} {user} {host} {password}')