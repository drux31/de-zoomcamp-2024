
q_lieux_2021 = """
    select 
        Num_Acc,
        catr,
        voie,
        v1,
        v2,
        circ,
        cast(nullif(nbv, '#ERREUR') as BIGINT) as nbv,
        vosp,
        prof,
        pr,
        pr1,
        plan,
        cast(replace(lartpc, ',', '.') as double) as lartpc,
        cast(replace(larrout, ',', '.') as double) as larrout,
        surf,
        infra,
        situ,
        vma
    from raw_data.lieux_2022
    
    """
q_lieux_2022 = """
    select 
        Num_Acc,
        catr,
        voie,
        v1,
        v2,
        circ,
        cast(nullif(nbv, '#ERREUR') as BIGINT) as nbv,
        vosp,
        prof,
        pr,
        pr1,
        plan,
        cast(replace(lartpc, ',', '.') as double) as lartpc,
        cast(replace(larrout, ',', '.') as double) as larrout,
        surf,
        infra,
        situ,
        vma
    from raw_data.lieux_2022
    
    """
q_lieux_2020 = """
    select 
        Num_Acc,
        catr,
        voie,
        v1,
        v2,
        circ,
        cast(nullif(nbv, '#ERREUR') as BIGINT) as nbv,
        vosp,
        prof,
        pr,
        pr1,
        plan,
        cast(replace(lartpc, ',', '.') as double) as lartpc,
        cast(replace(larrout, ',', '.') as double) as larrout,
        surf,
        infra,
        situ,
        vma
    from raw_data.lieux_2022
    
    """
q_lieux_2019 = """
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
    from raw_data.lieux_2019
    """

query_union_lieux = " ".join([q_lieux_2021, 
                       "union all by name",
                       q_lieux_2020,
                       "union all by name",
                       q_lieux_2022,
                       "union all by name",
                       q_lieux_2019])


query_union_usagers = " ".join([
            "select * from raw_data.usagers_2019",
            "union all by name",
            "select * from raw_data.usagers_2020",
            "union all by name",
            "select * from raw_data.usagers_2021",
            "union all by name",
            "select * from raw_data.usagers_2022"])