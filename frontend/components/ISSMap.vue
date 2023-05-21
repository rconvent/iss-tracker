<template>
    <div class="map-container">
        <div id="map"></div>
    </div>
</template>
  
<script>

import mapboxgl from 'mapbox-gl';

export default {
    data() {
        return {
            accessToken: 'pk.eyJ1IjoicmNvbnZlbnQiLCJhIjoiY2xodXB3eXI1MDI4OTNncGdpY2E4MndzZyJ9.4Cm9FftoMvjqw8xJf6DJGw',
            map: {}
        }
    },
    mounted() {
        this.createMap();
    },

    methods: {
        createMap() {
            mapboxgl.accessToken = this.accessToken
            const map = new mapboxgl.Map({
                container: 'map',
                style: 'mapbox://styles/mapbox/streets-v12',
                zoom: 2
            });

            map.on('load', async () => {
                const geojson = await getLocation();
                map.addSource('iss', {
                    type: 'geojson',
                    data: geojson
                });

                map.addLayer({
                    id: 'iss',
                    type: 'symbol',
                    source: 'iss',
                    layout: {
                        'icon-image': "rocket"
                    }
                });

                const updateSource = setInterval(async () => {
                    const geojson = await getLocation(updateSource);
                    map.getSource('iss').setData(geojson);
                }, 20000);

                async function getLocation(updateSource) {
                    try {
                        const response = await fetch('http://0.0.0.0:8000/iss/position/', { method: 'GET' });
                        const { latitude, longitude } = await response.json();

                        map.flyTo({
                            center: [longitude, latitude],
                            speed: 0.5
                        });

                        return {
                            type: 'FeatureCollection',
                            features: [
                                {
                                    type: 'Feature',
                                    geometry: {
                                        type: 'Point',
                                        coordinates: [longitude, latitude]
                                    }
                                }
                            ]
                        };
                    } catch (err) {
                        if (updateSource) clearInterval(updateSource);
                        throw new Error(err);
                    }
                }
            });
        }

    }

};
</script>
  
<style>
#map {
    position: absolute;
    top: 0;
    bottom: 0;
    width: 100%;
}
</style>