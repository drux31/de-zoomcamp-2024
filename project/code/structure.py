from pyspark.sql import types

schema = types.StructType([
    # General information
    types.StructField('code', types.StringType(), True), 
    types.StructField('url', types.StringType(), True), 
    types.StructField('creator', types.StringType(), True), 
    types.StructField('created_t', types.IntegerType(), True), # unix timestamp
    types.StructField('created_datetime', types.StringType(), True), 
    types.StructField('last_modified_t', types.IntegerType(), True), 
    types.StructField('last_modified_datetime', types.TimestampType(), True), 
    types.StructField('last_modified_by', types.StringType(), True), 
    types.StructField('last_updated_t', types.IntegerType(), True), 
    types.StructField('last_updated_datetime', types.TimestampType(), True), 
    types.StructField('product_name', types.StringType(), True), 
    types.StructField('abbreviated_product_name', types.StringType(), True), 
    types.StructField('generic_name', types.StringType(), True), 
    types.StructField('quantity', types.StringType(), True), 

    # tags
    types.StructField('packaging', types.StringType(), True), 
    types.StructField('packaging_tags', types.StringType(), True), 
    types.StructField('packaging_en', types.StringType(), True), 
    types.StructField('packaging_text', types.StringType(), True), 
    types.StructField('brands', types.StringType(), True), 
    types.StructField('brands_tags', types.StringType(), True), 
    types.StructField('categories', types.StringType(), True), 
    types.StructField('categories_tags', types.StringType(), True), 
    types.StructField('categories_en', types.StringType(), True), 
    types.StructField('origins', types.StringType(), True), 
    types.StructField('origins_tags', types.StringType(), True), 
    types.StructField('origins_en', types.StringType(), True), 
    types.StructField('manufacturing_places', types.StringType(), True), 
    types.StructField('manufacturing_places_tags', types.StringType(), True), 
    types.StructField('labels', types.StringType(), True), 
    types.StructField('labels_tags', types.StringType(), True), 
    types.StructField('labels_en', types.StringType(), True), 
    types.StructField('emb_codes', types.StringType(), True),
    types.StructField('emb_codes_tags', types.StringType(), True), 
    types.StructField('first_packaging_code_geo', types.StringType(), True), 
    types.StructField('cities', types.StringType(), True), 
    types.StructField('cities_tags', types.StringType(), True), 
    types.StructField('purchase_places', types.StringType(), True), 
    types.StructField('stores', types.StringType(), True), 
    types.StructField('countries', types.StringType(), True), 
    types.StructField('countries_tags', types.StringType(), True), 
    types.StructField('countries_en', types.StringType(), True), 

    # ingredients
    types.StructField('ingredients_text', types.StringType(), True), 
    types.StructField('ingredients_tags', types.StringType(), True), 
    types.StructField('ingredients_analysis_tags', types.StringType(), True), 
    types.StructField('allergens', types.StringType(), True), 
    types.StructField('allergens_en', types.StringType(), True), 
    types.StructField('traces', types.StringType(), True), 
    types.StructField('traces_tags', types.StringType(), True), 
    types.StructField('traces_en', types.StringType(), True), 

    # misc. data
    types.StructField('serving_size', types.FloatType(), True), 
    types.StructField('serving_quantity', types.FloatType(), True), 
    types.StructField('no_nutrition_data', types.StringType(), True), 
    types.StructField('additives_n', types.IntegerType(), True), 
    types.StructField('additives', types.StringType(), True), 
    types.StructField('additives_tags', types.StringType(), True), 
    types.StructField('additives_en', types.StringType(), True), 
    types.StructField('nutriscore_score', types.IntegerType(), True), 
    types.StructField('nutriscore_grade', types.StringType(), True), 
    types.StructField('nova_group', types.StringType(), True), 
    types.StructField('pnns_groups_1', types.StringType(), True), 
    types.StructField('pnns_groups_2', types.StringType(), True), 
    types.StructField('food_groups', types.StringType(), True), 
    types.StructField('food_groups_tags', types.StringType(), True), 
    types.StructField('food_groups_en', types.StringType(), True), 
    types.StructField('states', types.StringType(), True), 
    types.StructField('states_tags', types.StringType(), True), 
    types.StructField('states_en', types.StringType(), True), 
    types.StructField('brand_owner', types.StringType(), True), 
    types.StructField('ecoscore_score', types.StringType(), True), 
    types.StructField('ecoscore_grade', types.StringType(), True), 
    types.StructField('nutrient_levels_tags', types.StringType(), True), 
    types.StructField('product_quantity', types.FloatType(), True), 
    types.StructField('owner', types.StringType(), True), 
    types.StructField('data_quality_errors_tags', types.StringType(), True), 
    types.StructField('unique_scans_n', types.StringType(), True), 
    types.StructField('popularity_tags', types.StringType(), True), 
    types.StructField('completeness', types.FloatType(), True), 
    types.StructField('last_image_t', types.StringType(), True), 
    types.StructField('last_image_datetime', types.StringType(), True), 
    types.StructField('main_category', types.StringType(), True), 
    types.StructField('main_category_en', types.StringType(), True), 
    types.StructField('image_url', types.StringType(), True), 
    types.StructField('image_small_url', types.StringType(), True), 
    types.StructField('image_ingredients_url', types.StringType(), True), 
    types.StructField('image_ingredients_small_url', types.StringType(), True), 
    types.StructField('image_nutrition_url', types.StringType(), True), 
    types.StructField('image_nutrition_small_url', types.StringType(), True), 

    # nutrition facts
    types.StructField('energy-kj_100g', types.StringType(), True), 
    types.StructField('energy-kcal_100g', types.StringType(), True), 
    types.StructField('energy_100g', types.StringType(), True), 
    types.StructField('energy-from-fat_100g', types.StringType(), True), 
    types.StructField('fat_100g', types.StringType(), True), 
    types.StructField('saturated-fat_100g', types.StringType(), True), 
    types.StructField('butyric-acid_100g', types.StringType(), True), 
    types.StructField('caproic-acid_100g', types.StringType(), True), 
    types.StructField('caprylic-acid_100g', types.StringType(), True), 
    types.StructField('capric-acid_100g', types.StringType(), True), 
    types.StructField('lauric-acid_100g', types.StringType(), True), 
    types.StructField('myristic-acid_100g', types.StringType(), True), 
    types.StructField('palmitic-acid_100g', types.StringType(), True), 
    types.StructField('stearic-acid_100g', types.StringType(), True), 
    types.StructField('arachidic-acid_100g', types.StringType(), True), 
    types.StructField('behenic-acid_100g', types.StringType(), True), 
    types.StructField('lignoceric-acid_100g', types.StringType(), True), 
    types.StructField('cerotic-acid_100g', types.StringType(), True), 
    types.StructField('montanic-acid_100g', types.StringType(), True), 
    types.StructField('melissic-acid_100g', types.StringType(), True), 
    types.StructField('unsaturated-fat_100g', types.StringType(), True), 
    types.StructField('monounsaturated-fat_100g', types.StringType(), True), 
    types.StructField('omega-9-fat_100g', types.StringType(), True), 
    types.StructField('polyunsaturated-fat_100g', types.StringType(), True), 
    types.StructField('omega-3-fat_100g', types.StringType(), True), 
    types.StructField('omega-6-fat_100g', types.StringType(), True), 
    types.StructField('alpha-linolenic-acid_100g', types.StringType(), True), 
    types.StructField('eicosapentaenoic-acid_100g', types.StringType(), True), 
    types.StructField('docosahexaenoic-acid_100g', types.StringType(), True), 
    types.StructField('linoleic-acid_100g', types.StringType(), True), 
    types.StructField('arachidonic-acid_100g', types.StringType(), True), 
    types.StructField('gamma-linolenic-acid_100g', types.StringType(), True), 
    types.StructField('dihomo-gamma-linolenic-acid_100g', types.StringType(), True), 
    types.StructField('oleic-acid_100g', types.StringType(), True), 
    types.StructField('elaidic-acid_100g', types.StringType(), True), 
    types.StructField('gondoic-acid_100g', types.StringType(), True), 
    types.StructField('mead-acid_100g', types.StringType(), True), 
    types.StructField('erucic-acid_100g', types.StringType(), True), 
    types.StructField('nervonic-acid_100g', types.StringType(), True), 
    types.StructField('trans-fat_100g', types.StringType(), True), 
    types.StructField('cholesterol_100g', types.StringType(), True), 
    types.StructField('carbohydrates_100g', types.StringType(), True), 
    types.StructField('sugars_100g', types.StringType(), True), 
    types.StructField('added-sugars_100g', types.StringType(), True), 
    types.StructField('sucrose_100g', types.StringType(), True), 
    types.StructField('glucose_100g', types.StringType(), True), 
    types.StructField('fructose_100g', types.StringType(), True), 
    types.StructField('lactose_100g', types.StringType(), True), 
    types.StructField('maltose_100g', types.StringType(), True), 
    types.StructField('maltodextrins_100g', types.StringType(), True), 
    types.StructField('starch_100g', types.StringType(), True), 
    types.StructField('polyols_100g', types.StringType(), True), 
    types.StructField('erythritol_100g', types.StringType(), True), 
    types.StructField('fiber_100g', types.StringType(), True), 
    types.StructField('soluble-fiber_100g', types.StringType(), True), 
    types.StructField('insoluble-fiber_100g', types.StringType(), True), 
    types.StructField('proteins_100g', types.StringType(), True), 
    types.StructField('casein_100g', types.StringType(), True), 
    types.StructField('serum-proteins_100g', types.StringType(), True), 
    types.StructField('nucleotides_100g', types.StringType(), True), 
    types.StructField('salt_100g', types.StringType(), True), 
    types.StructField('added-salt_100g', types.StringType(), True), 
    types.StructField('sodium_100g', types.StringType(), True), 
    types.StructField('alcohol_100g', types.StringType(), True), 
    types.StructField('vitamin-a_100g', types.StringType(), True), 
    types.StructField('beta-carotene_100g', types.StringType(), True), 
    types.StructField('vitamin-d_100g', types.StringType(), True), 
    types.StructField('vitamin-e_100g', types.StringType(), True), 
    types.StructField('vitamin-k_100g', types.StringType(), True), 
    types.StructField('vitamin-c_100g', types.StringType(), True), 
    types.StructField('vitamin-b1_100g', types.StringType(), True), 
    types.StructField('vitamin-b2_100g', types.StringType(), True), 
    types.StructField('vitamin-pp_100g', types.StringType(), True),
    types.StructField('vitamin-b6_100g', types.StringType(), True), 
    types.StructField('vitamin-b9_100g', types.StringType(), True), 
    types.StructField('folates_100g', types.StringType(), True), 
    types.StructField('vitamin-b12_100g', types.StringType(), True), 
    types.StructField('biotin_100g', types.StringType(), True), 
    types.StructField('pantothenic-acid_100g', types.StringType(), True), 
    types.StructField('silica_100g', types.StringType(), True), 
    types.StructField('bicarbonate_100g', types.StringType(), True), 
    types.StructField('potassium_100g', types.StringType(), True), 
    types.StructField('chloride_100g', types.StringType(), True), 
    types.StructField('calcium_100g', types.StringType(), True), 
    types.StructField('phosphorus_100g', types.StringType(), True), 
    types.StructField('iron_100g', types.StringType(), True), 
    types.StructField('magnesium_100g', types.StringType(), True), 
    types.StructField('zinc_100g', types.StringType(), True), 
    types.StructField('copper_100g', types.StringType(), True), 
    types.StructField('manganese_100g', types.StringType(), True), 
    types.StructField('fluoride_100g', types.StringType(), True), 
    types.StructField('selenium_100g', types.StringType(), True), 
    types.StructField('chromium_100g', types.StringType(), True), 
    types.StructField('molybdenum_100g', types.StringType(), True), 
    types.StructField('iodine_100g', types.StringType(), True), 
    types.StructField('caffeine_100g', types.StringType(), True), 
    types.StructField('taurine_100g', types.StringType(), True), 
    types.StructField('ph_100g', types.StringType(), True), 

    # % of fruits, vegetables and nuts (excluding potatoes, yams, manioc)
    types.StructField('fruits-vegetables-nuts_100g', types.StringType(), True), 
    types.StructField('fruits-vegetables-nuts-dried_100g', types.StringType(), True), 
    types.StructField('fruits-vegetables-nuts-estimate_100g', types.StringType(), True), 
    types.StructField('fruits-vegetables-nuts-estimate-from-ingredients_100g', types.StringType(), True), 
    types.StructField('collagen-meat-protein-ratio_100g', types.StringType(), True), 
    types.StructField('cocoa_100g', types.StringType(), True), 
    types.StructField('chlorophyl_100g', types.StringType(), True), 
    types.StructField('carbon-footprint_100g', types.StringType(), True), 
    types.StructField('carbon-footprint-from-meat-or-fish_100g', types.StringType(), True), 
    types.StructField('nutrition-score-fr_100g', types.StringType(), True), 
    types.StructField('nutrition-score-uk_100g', types.StringType(), True), 
    types.StructField('glycemic-index_100g', types.StringType(), True), 
    types.StructField('water-hardness_100g', types.StringType(), True), 
    types.StructField('choline_100g', types.StringType(), True), 
    types.StructField('phylloquinone_100g', types.StringType(), True), 
    types.StructField('beta-glucan_100g', types.StringType(), True), 
    types.StructField('inositol_100g', types.StringType(), True), 
    types.StructField('carnitine_100g', types.StringType(), True), 
    types.StructField('sulphate_100g', types.StringType(), True), 
    types.StructField('nitrate_100g', types.StringType(), True), 
    types.StructField('acidity_100g', types.StringType(), True)
])