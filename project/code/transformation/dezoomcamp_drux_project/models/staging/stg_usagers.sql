{{ config(materialized="view") }}

select 
    Num_Acc as accident_id,
    id_vehicule as vehicule_id,
    place as occupied_place,    
    catu as user_catagory,      
    grav as wound_gravity,        
    case sexe
        when 1 then 'Masculin'
        when 2 then 'Feminin'
        else 'Inconnu'
    end as user_genre,        
    an_nais as birth_year,
    case trajet 
        when 1 then 'Domicile - travail' 
        when 2 then 'Domicile - école'
        when 3 then 'Courses'
        when 4 then 'Déplacement professionnel'
        when 5 then 'Loisirs'
        when 9 then 'Autre'
        else 'Non renseigné' 
    end as trajet_accident,      
from  {{ source("staging", "usagers_all") }}
where id_vehicule is not null;