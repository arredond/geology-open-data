/* Table to GeoJSON

Create a view of a table as a GeoJSON Feature Collection.
Used to retrieve data for the map.
*/

CREATE OR REPLACE VIEW {t}_geojson AS (
	SELECT
	json_build_object(
		'type', 'FeatureCollection',
		'features', json_agg(ST_AsGeoJSON(t.*)::json)
	) AS geojson
	FROM {t} t
);
