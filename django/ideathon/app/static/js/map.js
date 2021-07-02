let markers = [];
let markerIndex;
// 지번 주소 기준으로 중복 데이터 제거
let preMarkerAddr = [];
let mapContainer = document.getElementById('map'), // 지도를 표시할 div 
    mapOption = { 
        center: new kakao.maps.LatLng(37.29692790158919, 126.83433417582125), // 지도의 중심좌표
        level: 4 // 지도의 확대 레벨 
    }; 
// 지도를 생성합니다    
let map = new kakao.maps.Map(mapContainer, mapOption); 
// 장소 검색 객체를 생성합니다
var ps = new kakao.maps.services.Places();  
// 검색 결과 목록이나 마커를 클릭했을 때 장소명을 표출할 인포윈도우를 생성합니다
var infowindow = new kakao.maps.InfoWindow({zIndex:1});
// 접속 위치 변수
var locPosition;
// view에서 받아온 json파일
var detailData;
const detail = document.getElementById('placesList-detail-hos');
const nullList = document.getElementById('placesList-Null');
const returnToList = document.getElementById('totalList');
const pageNum = document.getElementById('pagination');

document.querySelector('.active').setAttribute('class', 'nav-link')
if (keyword == '약국') {
    document.getElementById('ph').setAttribute('class', 'nav-link active')
} else if (keyword == '응급실') {
    document.getElementById('em').setAttribute('class', 'nav-link active')
} else if (keyword) {
    document.getElementById('ho').setAttribute('class', 'nav-link active')
}

// HTML5의 geolocation으로 사용할 수 있는지 확인합니다 
if (navigator.geolocation) {
    // GeoLocation을 이용해서 접속 위치를 얻어옵니다
    navigator.geolocation.getCurrentPosition(function(position) {
        var lat = position.coords.latitude, // 위도
            lon = position.coords.longitude; // 경도
        locPosition = new kakao.maps.LatLng(lat, lon); // 마커가 표시될 위치를 geolocation으로 얻어온 좌표로 생성합니다

        displayMarker(locPosition);
        // 지도 중심좌표를 접속위치로 변경합니다
        map.setCenter(locPosition);
        searchPlaces(keyword)
    });

} else { // HTML5의 GeoLocation을 사용할 수 없을때 마커 표시 위치를 설정합니다
    locPosition = new kakao.maps.LatLng(37.29692790158919, 126.83433417582125);
    displayMarker(locPosition);
    // 지도 중심좌표를 접속위치로 변경합니다
    map.setCenter(locPosition);
    searchPlaces(keyword)
}

document.getElementById('reSearch').addEventListener('click', function(){
    searchPlaces(keyword)
})

document.getElementById('nowPlace').addEventListener('click', function(){
    map.panTo(locPosition);
})

// 키워드 검색을 요청하는 함수입니다
function searchPlaces(value) {
    detail.style.display = "none";
    nullList.style.display = 'none';
    keyword = value;

    // 장소검색 객체를 통해 키워드로 장소검색을 요청합니다
    ps.keywordSearch(keyword, placesSearchCB, {bounds : map.getBounds()}); 
}

// 장소검색이 완료됐을 때 호출되는 콜백함수 입니다
function placesSearchCB(data, status, pagination) {
    if (status === kakao.maps.services.Status.OK) {

        // 정상적으로 검색이 완료됐으면
        // 검색 목록과 마커를 표출합니다
        displayPlaces(data);

        // 페이지 번호를 표출합니다
        displayPagination(pagination);

    } else if (status === kakao.maps.services.Status.ZERO_RESULT) {

        var mapOption = { 
            center: map.getCenter(),
            level: map.getLevel()
        }; 
        mapOption.level++;
        map = new kakao.maps.Map(mapContainer, mapOption);
        displayMarker(locPosition);
        ps = new kakao.maps.services.Places(map);
        ps.keywordSearch(keyword, placesSearchCB, {bounds : map.getBounds()});

    } else if (status === kakao.maps.services.Status.ERROR) {

        alert('검색 결과 중 오류가 발생했습니다.');
        return;

    }
}

// 검색 결과 목록과 마커를 표출하는 함수입니다
function displayPlaces(places) {

    var listEl = document.getElementById('placesList'), 
    menuEl = document.getElementById('placesList'),
    fragment = document.createDocumentFragment(), 
    bounds = new kakao.maps.LatLngBounds(), 
    listStr = '';
    
    // 검색 결과 목록에 추가된 항목들을 제거합니다
    removeAllChildNods(listEl);

    // 지도에 표시되고 있는 마커를 제거합니다
    removeMarker();
    preMarkerAddr = [];
    markerIndex = 0;
    for ( var i=0; i<places.length; i++ ) {
        if ( places[i].place_name.indexOf('코로나') == -1 ) {
            if (places[i].place_name.indexOf('떡볶이') == -1 ) {
                if (places[i].place_name.indexOf('은행') == -1 ) {
                    if (preMarkerAddr.indexOf(places[i].address_name) == -1) {
                        // 마커를 생성하고 지도에 표시합니다
                        var placePosition = new kakao.maps.LatLng(places[i].y, places[i].x),
                            marker = addMarker(placePosition, markerIndex), 
                            itemEl = getListItem(markerIndex, places[i]); // 검색 결과 항목 Element를 생성합니다
                        // 검색된 장소 위치를 기준으로 지도 범위를 재설정하기위해
                        // LatLngBounds 객체에 좌표를 추가합니다
                        // bounds.extend(placePosition);
                        preMarkerAddr.push(places[i].address_name);
                        // 마커와 검색결과 항목에 mouseover 했을때
                        // 해당 장소에 인포윈도우에 장소명을 표시합니다
                        // mouseout 했을 때는 인포윈도우를 닫습니다
                        (function(marker, title) {
                            var markerPosition = placePosition
                            kakao.maps.event.addListener(marker, 'mouseover', function() {
                                displayInfowindow(marker, title);
                            });

                            kakao.maps.event.addListener(marker, 'mouseout', function() {
                                infowindow.close();
                            });
                        })(marker, places[i].place_name);

                        fragment.appendChild(itemEl);
                    }
                }
            }
        }
    }

    // 검색결과 항목들을 검색결과 목록 Elemnet에 추가합니다
    listEl.appendChild(fragment);
    menuEl.scrollTop = 0;

    // 검색된 장소 위치를 기준으로 지도 범위를 재설정합니다
    //map.setBounds(bounds);
}

// 검색결과 항목을 Element로 반환하는 함수입니다
function getListItem(index, places) {
    var markerPosition = new kakao.maps.LatLng(places.y, places.x);
    var box = document.createElement('div');
    var el = document.createElement('li'),

    itemStr = '<span class="markerbg marker_' + (index+1) + '"></span>' +
                '<div class="info">' +
                '   <h5 class="info-name">' + places.place_name + '</h5>';

    if (places.road_address_name) {
        var place_name =  `${places.place_name}`.replace(/ /g, "+");
        var road_address_name = `${places.road_address_name}`.replace(/ /g, "+");
        box.onclick = function(event) {
            event.stopPropagation() 
            map.panTo(markerPosition);
            getData(road_address_name,place_name);
        }
        itemStr += '    <span>' + places.road_address_name + '</span>' +
                    '   <span class="jibun gray">' +  places.address_name  + '</span>';
        
    } else {
        var place_name =  `${places.place_name}`.replace(/ /g, "+");
        var address_name = `${places.address_name}`.replace(/ /g, "+");
        box.onclick = function(event) { 
            event.stopPropagation()
            map.panTo(markerPosition);
            getData(address_name,place_name);
        }

        itemStr += '    <span>' +  places.address_name  + '</span>'; 
    }

    itemStr += '  <span>' + places.phone  + '</span>' +
                '</div>';           

    el.innerHTML = itemStr;
    el.className = 'item';
    box.className = 'box';

    box.appendChild(el);
    markerIndex++;

    return box;
}


// 마커를 생성하고 지도 위에 마커를 표시하는 함수입니다
function addMarker(position, idx, title) {
    var imageSrc = 'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_number_blue.png', // 마커 이미지 url, 스프라이트 이미지를 씁니다
        imageSize = new kakao.maps.Size(36, 37),  // 마커 이미지의 크기
        imgOptions =  {
            spriteSize : new kakao.maps.Size(36, 691), // 스프라이트 이미지의 크기
            spriteOrigin : new kakao.maps.Point(0, (idx*46)+10), // 스프라이트 이미지 중 사용할 영역의 좌상단 좌표
            offset: new kakao.maps.Point(13, 37) // 마커 좌표에 일치시킬 이미지 내에서의 좌표
        },
        markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize, imgOptions),
            marker = new kakao.maps.Marker({
            position: position, // 마커의 위치
            image: markerImage 
        });

    marker.setMap(map); // 지도 위에 마커를 표출합니다
    markers.push(marker);  // 배열에 생성된 마커를 추가합니다

    return marker;
}

// 지도 위에 표시되고 있는 마커를 모두 제거합니다
function removeMarker() {
    for ( var i = 0; i < markers.length; i++ ) {
        markers[i].setMap(null);
    }   
    markers = [];
}

// 검색결과 목록 하단에 페이지번호를 표시는 함수입니다
function displayPagination(pagination) {
    var paginationEl = document.getElementById('pagination'),
        fragment = document.createDocumentFragment(),
        i; 

    // 기존에 추가된 페이지번호를 삭제합니다
    while (paginationEl.hasChildNodes()) {
        paginationEl.removeChild (paginationEl.lastChild);
    }

    for (i=1; i<=pagination.last; i++) {
        var el = document.createElement('a');
        el.href = "#";
        el.innerHTML = i;

        if (i===pagination.current) {
            el.className = 'on';
        } else {
            el.onclick = (function(i) {
                return function() {
                    pagination.gotoPage(i);
                }
            })(i);
        }

        fragment.appendChild(el);
    }
    paginationEl.appendChild(fragment);
}

// 검색결과 목록 또는 마커를 클릭했을 때 호출되는 함수입니다
// 인포윈도우에 장소명을 표시합니다
function displayInfowindow(marker, title) {
    var content = '<div style="padding:5px;z-index:1;">' + title + '</div>';

    infowindow.setContent(content);
    infowindow.open(map, marker);
}

 // 검색결과 목록의 자식 Element를 제거하는 함수입니다
function removeAllChildNods(el) {   
    while (el.hasChildNodes()) {
        el.removeChild (el.lastChild);
    }
}

// 지도에 마커를 표시하는 함수입니다
function displayMarker(locPosition) {
    // 마커를 생성합니다
    var marker = new kakao.maps.Marker({  
        map: map, 
        position: locPosition
    });
    marker.setMap(map);
}    

// map 페이지에서 키워드 검색 함수
var searchButton = document.querySelector('.search_button')


function startSearch(value) {
    detail.style.display = 'none'
    document.getElementById("placesList").style.display = "block";
    document.getElementById("pageNum").style.display = "block";
    document.getElementById("placesList-detail-emer").style.display = "none";
    document.getElementById("placesList-detail-phar").style.display = "none";
    nullList.style.display = 'none'
    searchPlaces(value);
};

/*
searchButton.addEventListener('click', function() {
    var keyword = document.getElementById("searchKeyword").value;
    startSearch(keyword);
});
*/
// httpRequest로 크롤링된 데이터 json형식으로 수신
function getData(addr, name) {
    var httpRequest = new XMLHttpRequest();
    var url = './' + addr + '/' + name + '/';
    httpRequest.open('GET', url);
    httpRequest.onreadystatechange = function() {
        if(this.status == 200 && this.readyState == this.DONE){
            // 요청한 데이터를 반환
            detailData = JSON.parse(httpRequest.response);
            showListDetail(detailData, name, addr);
        } else if (this.status != 200){ 
            nullList.style.display = 'block';
            returnToList.style.display = "block";
        }
    };
    httpRequest.send()
}

// map.html detail창 구현
function showListDetail(data, name, addr) {
    var name = name.replace(/\+/g, ' ')
    var addr = addr.replace(/\+/g, ' ')
    if (!data) {
        nullList.style.display = 'block';
        returnToList.style.display = "block";
    } else if (data.keyword) {
        // 동기처리 - detail창 요소 구성 전까지 노출되지 않음.
        new Promise((resolve, reject) => {
            createDetailBox(data, name, addr)
            resolve()
        })
        .then(() => {
            returnToList.style.display = "block";
            if (data.keyword == '응급실') {
                document.getElementById("placesList-detail-emer").style.display = "block";
            } else if (data.keyword == '약국') {
                document.getElementById("placesList-detail-phar").style.display = "block";
            } else {
                detail.style.display = "block";
            }
            document.getElementById("placesList").style.display = "none";
            document.getElementById("pageNum").style.display = "none";
        })
        .catch((error) => {
            console.log(error)
            console.log('showDetail Error');
        })
    } else {
        
    }
}

function createDetailBox(data, name, addr) {
    if (data.keyword == '응급실') {
        var dgid = data.dgid.replace(/\,/g, ' ')
        document.querySelector('.title').innerText = name
        document.querySelector('.addr').innerText = addr
        document.querySelector('.dutytel3').innerText = data.dutyTel3
        document.querySelector('.hvdnm').innerText = data.hvdnm
        document.querySelector('.hv1').innerText = data.hv1
        document.querySelector('.hvec').innerText = data.hvec
        document.querySelector('.hvgc').innerText = data.hvgc
        document.querySelector('.hvoc').innerText = data.hvoc
        document.querySelector('.hvicc').innerText = data.hvicc
        document.querySelector('.hvccc').innerText = data.hvccc
        document.querySelector('.hvccc').innerText = data.hvccc
        document.querySelector('.hv7').innerText = data.hv7
        document.querySelector('.hv8').innerText = data.hv9
        document.querySelector('.hv2').innerText = data.hv2
        document.querySelector('.hv3').innerText = data.hv3
        document.querySelector('.hv4').innerText = data.hv4
        document.querySelector('.hvncc').innerText = data.hvncc
        document.querySelector('.hvamyn').innerText = data.hvamyn
        document.querySelector('.hvctayn').innerText = data.hvctayn
        document.querySelector('.hvmriayn').innerText = data.hvmriayn
        document.querySelector('.dgid').innerText = dgid
    } else if (data.keyword == '약국') {
        document.querySelector('.ptitle').innerText = name
        document.querySelector('.paddr').innerText = data.dutyAddr
        document.querySelector('.pTele').innerText = data.dutyTel1

        document.querySelector('.dutyTime1').innerText = data.dutyTime1s.slice(0,2) +':'+ data.dutyTime1s.slice(2,5) +"~"+data.dutyTime1c.slice(0,2) +':'+ data.dutyTime1c.slice(2,5)
        document.querySelector('.dutyTime2').innerText = data.dutyTime2s.slice(0,2) +':'+ data.dutyTime2s.slice(2,5) +"~"+data.dutyTime2c.slice(0,2) +':'+ data.dutyTime2c.slice(2,5)
        document.querySelector('.dutyTime3').innerText = data.dutyTime3s.slice(0,2) +':'+ data.dutyTime3s.slice(2,5) +"~"+data.dutyTime3c.slice(0,2) +':'+ data.dutyTime3c.slice(2,5)
        document.querySelector('.dutyTime4').innerText = data.dutyTime4s.slice(0,2) +':'+ data.dutyTime4s.slice(2,5) +"~"+data.dutyTime4c.slice(0,2) +':'+ data.dutyTime4c.slice(2,5)
        document.querySelector('.dutyTime5').innerText = data.dutyTime5s.slice(0,2) +':'+ data.dutyTime5s.slice(2,5) +"~"+data.dutyTime5c.slice(0,2) +':'+ data.dutyTime5c.slice(2,5)
        document.querySelector('.dutyTime6').innerText = data.dutyTime6s.slice(0,2) +':'+ data.dutyTime6s.slice(2,5) +"~"+data.dutyTime6c.slice(0,2) +':'+ data.dutyTime6c.slice(2,5)
        document.querySelector('.dutyTime7').innerText = data.dutyTime7s.slice(0,2) +':'+ data.dutyTime7s.slice(2,5) +"~"+data.dutyTime7c.slice(0,2) +':'+ data.dutyTime7c.slice(2,5)
        document.querySelector('.dutyTime8').innerText = data.dutyTime8s.slice(0,2) +':'+ data.dutyTime8s.slice(2,5) +"~"+data.dutyTime8c.slice(0,2) +':'+ data.dutyTime8c.slice(2,5)

    } else {
        var dgid = data.dgidIdName.replace(/\,/g, ' ')
        document.querySelector('.htitle').innerText = name
        document.querySelector('.haddr').innerText = data.dutyAddr
        document.querySelector('.hTele').innerText = data.dutyTel1
        document.querySelector('.hdgid').innerText = dgid

        document.querySelector('.hdutyTime1').innerText = data.dutyTime1s.slice(0,2) +':'+ data.dutyTime1s.slice(2,5) +"~"+data.dutyTime1c.slice(0,2) +':'+ data.dutyTime1c.slice(2,5)
        document.querySelector('.hdutyTime2').innerText = data.dutyTime2s.slice(0,2) +':'+ data.dutyTime2s.slice(2,5) +"~"+data.dutyTime2c.slice(0,2) +':'+ data.dutyTime2c.slice(2,5)
        document.querySelector('.hdutyTime3').innerText = data.dutyTime3s.slice(0,2) +':'+ data.dutyTime3s.slice(2,5) +"~"+data.dutyTime3c.slice(0,2) +':'+ data.dutyTime3c.slice(2,5)
        document.querySelector('.hdutyTime4').innerText = data.dutyTime4s.slice(0,2) +':'+ data.dutyTime4s.slice(2,5) +"~"+data.dutyTime4c.slice(0,2) +':'+ data.dutyTime4c.slice(2,5)
        document.querySelector('.hdutyTime5').innerText = data.dutyTime5s.slice(0,2) +':'+ data.dutyTime5s.slice(2,5) +"~"+data.dutyTime5c.slice(0,2) +':'+ data.dutyTime5c.slice(2,5)
        document.querySelector('.hdutyTime6').innerText = data.dutyTime6s.slice(0,2) +':'+ data.dutyTime6s.slice(2,5) +"~"+data.dutyTime6c.slice(0,2) +':'+ data.dutyTime6c.slice(2,5)
        document.querySelector('.hdutyTime7').innerText = data.dutyTime7s.slice(0,2) +':'+ data.dutyTime7s.slice(2,5) +"~"+data.dutyTime7c.slice(0,2) +':'+ data.dutyTime7c.slice(2,5)
        document.querySelector('.hdutyTime8').innerText = data.dutyTime8s.slice(0,2) +':'+ data.dutyTime8s.slice(2,5) +"~"+data.dutyTime8c.slice(0,2) +':'+ data.dutyTime8c.slice(2,5)
    }
}

returnToList.addEventListener('click', function() {
    this.style.display = 'none'
    detail.style.display = 'none'
    document.getElementById("placesList").style.display = "block";
    document.getElementById("pageNum").style.display = "block";
    
    document.getElementById("placesList-detail-emer").style.display = "none";
    document.getElementById("placesList-detail-phar").style.display = "none";
    nullList.style.display = 'none'
})