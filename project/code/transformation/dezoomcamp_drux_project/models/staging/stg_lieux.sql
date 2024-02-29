{{ config(materialized="view") }}

select 
    Num_Acc as accident_id,
    case catr
        when 1 then 'Autoroute'
        when 2 then 'Nationale'
        when 3 then 'Départementale'
        when 4 then 'Communales'
        when 5 then 'Hors réseau public'
        when 6 then 'Parkings'
        when 7 then 'Villes'
        when 9 then 'Autre'
        else 'Non renseigné'
    end as categorie_route,
    voie as numero_route,
    vma as vitesse_max
from  {{ source("staging", "lieux_all") }}