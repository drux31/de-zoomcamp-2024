{{ config(materialized="view") }}

select 
    Num_Acc as accident_id,
    Accident_date as accident_date,
    case lum 
        when 1 then 'Plein jour'
        when 2 then 'Aube'
        when 3 then 'Nuit sans éclairage'
        when 4 then 'Nuit avec éclairage éteint'
        when 5 then 'Nuit avec éclairage allumé'
        else 'Inconnu'
    end as condition_eclairage,
    dep as departement,
    com as commune,
    case agg
        when 1 then 'Hors agglomération'
        when 2 then 'En agglomération'
        else 'Inconnu'
    end as localisation,
    --int,
    case atm 
        when 1 then 'Normale'
        when 2 then 'Pluie légère'
        when 3 then 'Pluie forte'
        when 4 then 'Neige - grêle'
        when 5 then 'Brouillard'
        when 6 then 'Tempête'
        when 8 then 'Temps couvert'
        when 7 then 'Temps éblouissant'
        else 'Non renseigné'
    end as cond_atmospherique,
    adr as adresse_postale,
    latitude,
    longitude
from  {{ source("staging", "caracteristiques_all") }}