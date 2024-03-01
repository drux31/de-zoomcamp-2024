with donnees_vehicules as (

    select *
    from {{ ref("stg_vehicules") }}
    where description_motirisation != 'Inconnue'
),
donnees_lieux as (

    select *
    from {{ ref("stg_lieux") }}
    where categorie_route != 'Non renseigné'   
),
donnees_caracteristiques as (

    select * 
    from {{ ref("stg_caracterisques") }}
    where accident_date is not null
),
donnees_usagers as (

    select *
    from {{ ref("stg_usagers") }}
),
dim_categ_vhl as (

    select *
    from {{ ref("dim_categories_vhl") }}
),
dim_communes as (

    select *
    from {{ ref("dim_communes") }}
),
dim_dpt as (

    select *
    from {{ ref("dim_departements") }}
)
select 
    ca.accident_id,
    ca.accident_date,
    ca.cond_atmospherique,
    ca.condition_eclairage,
    dl.categorie_route,
    dp.nom_departement,
    dp.nom_region,
    dc.nom_commune,
    ca.latitude,
    ca.longitude,
    dv.motorisation,
    dv.description_motirisation,
    dv.nb_occupant as nb_occupant_vhl_public,
    du.annee_naissance as annee_naissance_usager,
    du.genre_usager,
    du.gravite_blessure,
    du.categorie_usager,
    du.trajet_accident
from donnees_caracteristiques ca
join dim_dpt dp on dp.code_departement = ca.departement
join dim_communes dc on (dc.code_departement = dp.code_departement and dc.code_commune = ca.commune)
join donnees_lieux dl on dl.accident_id = ca.accident_id
join donnees_usagers du on du.accident_id = ca.accident_id
join donnees_vehicules dv on (dv.accident_id = ca.accident_id and du.vehicule_id = dv.vehicule_id)


