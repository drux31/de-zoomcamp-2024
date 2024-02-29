{{ config(materialized="view") }}

select 
    Num_Acc as accident_id,
    id_vehicule as vehicule_id, 
    catv as code_categorie_vhl,
    case motor 
        when 1 then 'Hydrocarbures'
        when 2 then 'Hybride'
        when 3 then 'Electrique'
        when 4 then 'Hydrogène'
        when 5 then 'Humaine'
        when 6 then 'Autre'
        else 'Inconuue'
    end as motorisation,
    occutc as nb_occupant
from {{ source("staging", "vehicules_all") }}