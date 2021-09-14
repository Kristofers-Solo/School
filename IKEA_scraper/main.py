import eel
from ikea import *

eel.init('web')


@eel.expose
def call_in_js(product):
	product_names = {
	    "armchairs": arm_chairs,
	    "bathroom furniture": bathroom_furniture,
	    "bathroom lightning": bathroom_lighting,
	    "bed frames": bed_frames,
	    "bookcases": bookcases,
	    "boxes and baskets": boxes_and_baskets,
	    "candles": candles,
	    "ceiling lamps and spotlight": ceiling_lamps_and_spotlights,
	    "chairs and benches": chairs_and_benches,
	    "chest of drawers": chest_of_drawers,
	    "children's storage furniture": children_storage_furniture,
	    "curtains": curtains,
	    "day beds": day_beds,
	    "dining tables": dining_tables,
	    "dinnerware and serving": dinnerware_and_serving,
	    "glasses": glasses,
	    "home desks": home_desks,
	    "interior organisers": interior_organisers,
	    "kitchen interior organisers": kitchen_interior_organisers,
	    "light bulbs": light_bulbs,
	    "mattresses": mattresses,
	    "mirrors": mirrors,
	    "office chairs": office_chairs,
	    "office desks and tables": office_desks_and_tables,
	    "open shelving units": open_shelving_units,
	    "pax wardrobes": pax_wardrobes,
	    "pendant lamps": pendant_lamps,
	    "pillows": pillows,
	    "pots": pots,
	    "quilt covers and pillow cases": quilt_covers_and_pillow_cases,
	    "quilts": quilts,
	    "rugs": rugs,
	    "sheets and pillow cases": sheets_and_pillow_cases,
	    "sofa beds and chair beds": sofa_beds_and_chair_beds,
	    "sofa tables": sofa_tables,
	    "solitaire cabinets": solitaire_cabinets,
	    "solitaire wardrobes": solitaire_wardrobes,
	    "system cabinets": system_cabinets,
	    "table lamps": table_lamps,
	    "towels": towels,
	    "toys for small children": toys_for_small_children,
	    "tv benches": tv_benches
	}

	return product_names.get(product.strip().lower()).get_data()


eel.start('index.html', size=(500, 500))
