-- ============================================
-- SQL exploration: спринт 1
-- Разведочные запросы на датасете Berka
-- ============================================

-- 1. Базовые SELECT/COUNT
SELECT COUNT(*) FROM client;
SELECT COUNT(*) FROM trans;

-- 2. Пол клиента из birth_number (ГГММДД, у женщин +50 к месяцу)
SELECT
    birth_number,
    CASE
        WHEN SUBSTRING(birth_number::TEXT FROM 3 FOR 2)::INT > 50 THEN 'F'
        ELSE 'M'
    END AS gender
FROM client;

-- Распределение по полу
SELECT
    CASE
        WHEN SUBSTRING(birth_number::TEXT FROM 3 FOR 2)::INT > 50 THEN 'F'
        ELSE 'M'
    END AS gender,
    COUNT(*)
FROM client
GROUP BY gender;
-- M: 2724, F: 2645

-- 3. JOIN client + disp: кто владелец счёта, кто доверенное лицо
SELECT c.client_id, c.district_id, d.account_id, d.type
FROM client c
JOIN disp d ON c.client_id = d.client_id;

-- Распределение по типу владения
SELECT type, COUNT(*) FROM disp GROUP BY type;
-- OWNER: 4500, DISPONENT: 869

-- 4. Последний баланс по счёту через оконную функцию ROW_NUMBER
-- (balance — снимок остатка после транзакции, не суммируется —
--  нужна именно последняя по дате строка на каждый account_id)
SELECT c.client_id, latest.balance
FROM client c
JOIN disp d ON d.client_id = c.client_id
JOIN (
    SELECT account_id, balance,
           ROW_NUMBER() OVER (PARTITION BY account_id ORDER BY date DESC) AS rn
    FROM trans
) latest ON latest.account_id = d.account_id
WHERE latest.rn = 1;

-- Наблюдение: некоторые client_id дают одинаковый balance —
-- совместные счета (OWNER + DISPONENT на одном account_id)