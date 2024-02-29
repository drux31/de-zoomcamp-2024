{{ config(materialized="view") }}

select 
    Num_Acc as accident_id,
    id_vehicule as vehicule_id, 
    catv as categorie_vehicule,
    obs,
    obsm,
    choc,
    manv,
    motor,
    occutc
from {{ source("staging", "vehicules_all") }}