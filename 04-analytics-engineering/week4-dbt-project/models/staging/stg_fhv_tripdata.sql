with 

source as (

    select * from {{ source('staging', 'external_fhv_tripdata_all') }}

),

renamed as (

    select
        dispatching_base_num,
        pickup_datetime,
        dropoff_datetime,
        pulocationid as pickup_locationid,
        dolocationid as dropoff_locationid,
        sr_flag as sharedride_flag,
        affiliated_base_number

    from source

)

select * from renamed
