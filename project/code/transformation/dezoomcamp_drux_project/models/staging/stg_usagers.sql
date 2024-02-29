{{ config(materialized="view") }}

select 
    Num_Acc as accident_id,
    id_vehicule as vehicule_id,
    case catu 
        when 1 then 'Conducteur'
        when 2 then 'Passager'
        when 3 then 'Piéton'
        else 'Inconnue'
    end as categorie_usager,      
    case grav 
        when 1 then 'Indemne'
        when 2 then 'Tué'
        when 3 then 'Blessé hospitalisé'
        when 4 then 'Blessé léger'
        else 'Inconnue'
    end as gravite_blessure,        
    case sexe
        when 1 then 'Masculin'
        when 2 then 'Feminin'
        else 'Inconnu'
    end as genre_usager,        
    an_nais as annee_naissance,
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
where id_vehicule is not null