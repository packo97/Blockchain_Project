create table Block
(
    hash           VARCHAR(256),
    seed           integer,
    miner_address  VARCHAR(256),
    lottery_number integer
);

create table "Transaction"
(
    timestamp_transaction VARCHAR(50),
    event                 VARCHAR(150),
    vote                  int,
    address               VARCHAR(256),
    block_hash            VARCHAR(256)
        constraint Transaction_Block_hash_fk
            references Block (hash)
);


