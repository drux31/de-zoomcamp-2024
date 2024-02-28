select 
    Num_Acc,
    id_vehicule,
    num_veh,
    place,    
    catu,      
    grav,        
    sexe,        
    an_nais,
    trajet,      
    secu1,       
    secu2,       
    secu3,       
    locp,        
    actp,        
    etatp
from usagers_2019
limit 10;

select * from raw_data.usagers_2019
union all by name
select * from raw_data.usagers_2020
union all by name
select * from raw_data.usagers_2021
union all by name
select * from raw_data.usagers_2022

select * from raw_data.lieux_2019
union all by name
select * from raw_data.lieux_2020
union all by name
select * from raw_data.lieux_2021
union all by name
select * from raw_data.lieux_2022

select 
    Num_Acc,
    catr,
    voie,
    v1,
    v2,
    circ,
    nbv,
    vosp,
    prof,
    pr,
    pr1,
    plan,
    lartpc,
    larrout,
    surf,
    infra,
    situ,
    vma
from select * from raw_data.lieux_2022
limit 10