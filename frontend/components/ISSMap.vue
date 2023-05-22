<template>
                <div id="map-container">
                    <div id="map"></div>
                                            <div class="calculation-box">
                                                <p>Click the map to draw a polygon.</p>
                                                <div id="calculated-area"></div>
                                            </div>
                                    </div>
</template>
<script>
import MapboxDraw from "@mapbox/mapbox-gl-draw";
import mapboxgl from 'mapbox-gl';

import 'mapbox-gl/dist/mapbox-gl.css';

export default {
    data() {
        return {
            accessToken:
                'pk.eyJ1IjoicmNvbnZlbnQiLCJhIjoiY2xodXB3eXI1MDI4OTNncGdpY2E4MndzZyJ9.4Cm9FftoMvjqw8xJf6DJGw',
            map: {},
        }
    },
    mounted() {
        this.createMap()
    },

    methods: {
        createMap() {
            mapboxgl.accessToken = this.accessToken
            const map = new mapboxgl.Map({
                container: 'map',
                style: 'mapbox://styles/mapbox/streets-v12',
                zoom: 2,
            })

            map.on('load', async () => {
                const geojson = await getLocation()
                map.addSource('iss', {
                    type: 'geojson',
                    data: geojson,
                })

                map.addLayer({
                    id: 'iss_position',
                    type: 'symbol',
                    source: 'iss',
                    layout: {
                        'icon-image': 'rocket',
                    },
                })

                const popup = new mapboxgl.Popup({
                    closeButton: false,
                    closeOnClick: false
                });

                map.on('mouseenter', 'iss_position', (e) => {
                    map.getCanvas().style.cursor = 'pointer'

                    const coordinates = e.features[0].geometry.coordinates.slice()
                    const sunExposure = e.features[0].properties.sunExposure

                    while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
                        coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360
                    }


                    popup.setLngLat([coordinates[0], coordinates[1]])
                        .setHTML(
                            `${sunExposure}`
                        )
                        .addTo(map)
                })

                map.on('mouseleave', 'iss_position', () => {
                    map.getCanvas().style.cursor = ''
                    popup.remove()
                })

                const updateSource = setInterval(async () => {
                    const geojson = await getLocation(updateSource)
                    map.getSource('iss').setData(geojson)
                }, 20000)

                const draw = new MapboxDraw({
                    displayControlsDefault: false,
                    // Select which mapbox-gl-draw control buttons to add to the map.
                    controls: {
                        polygon: true,
                        trash: true
                    },
                    // Set mapbox-gl-draw to draw by default.
                    // The user does not have to click the polygon control button first.
                    defaultMode: 'draw_polygon'
                });
                map.addControl(draw);

                map.on('draw.create', updateArea);
                map.on('draw.delete', updateArea);
                map.on('draw.update', updateArea);

                // function updateArea(e) {
                //     const data = draw.getAll();
                //     const answer = document.getElementById('calculated-area');
                //     console.log(data)
                //     if (data.features.length > 0) {
                //         const area = turf.area(data);
                //         // Restrict the area to 2 decimal points.
                //         const rounded_area = Math.round(area * 100) / 100;
                //         answer.innerHTML = `<p><strong>${rounded_area}</strong></p><p>square meters</p>`;
                //     } else {
                //         answer.innerHTML = '';
                //         if (e.type !== 'draw.delete')
                //             alert('Click the map to draw a polygon.');
                //     }
                // }

                async function getLocation(updateSource) {
                    try {
                        const positionResponse = await fetch(
                            'http://0.0.0.0:8000/iss/position/',
                            { method: 'GET' }
                        )
                        const { latitude, longitude } = await positionResponse.json()

                        var dayBefore = new Date()
                        dayBefore.setDate(dayBefore.getDate() - 1)
                        dayBefore = dayBefore.toISOString().split('T')[0]
                        const exposureResponse = await fetch(
                            `http://0.0.0.0:8000/iss/sun/?from_date=${dayBefore}`,
                            { method: 'GET' }
                        )
                        const sunExposure = await exposureResponse.json()


                        map.flyTo({
                            center: [longitude, latitude],
                            speed: 0.5,
                        })

                        return {
                            type: 'FeatureCollection',
                            features: [
                                {
                                    type: 'Feature',
                                    geometry: {
                                        type: 'Point',
                                        coordinates: [longitude, latitude],
                                    },
                                    properties: {
                                        sunExposure:
                                            `<h1>ISS Sun Exposure : </h1>
                                            <ul>
                                            ${sunExposure.map((interval) => `<li>${interval}</li>`).join('')}
                                            </ul>
                                            `,
                                    },
                                },
                            ],
                        }
                    } catch (err) {
                        if (updateSource) clearInterval(updateSource)
                        throw new Error(err)
                    }
                }
            })
        },
    },
}
</script>

<style>
#map-container {
    position: relative;
    width: 100%;
    height: 100vh;
}

#map {
    position: absolute;
    top: 0;
    bottom: 0;
    width: 100%;
    height: 100%;
}

.mapboxgl-popup {
    position: absolute;
    max-width: 400px;
    font: 12px/20px 'Helvetica Neue', Arial, Helvetica, sans-serif;
}

.calculation-box {
    height: 75px;
    width: 150px;
    position: absolute;
    bottom: 40px;
    left: 10px;
    background-color: rgba(255, 255, 255, 0.9);
    padding: 15px;
    text-align: center;
}
 
p {
    font-family: 'Open Sans';
    margin: 0;
    font-size: 13px;
}
</style>