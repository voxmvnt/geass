function searchApi() {
    let searchValue = $('#search-input').val().trim();
    if (searchValue.length > 1){
        location.href = "/trend/search/" + searchValue + "/";
    }else{
        showAlertModal('검색어 (' + searchValue + ')가 너무 짧습니다.');
    }
}

document.getElementById('search-input').addEventListener('keyup', function(event){
    if (event.key === 'Enter'){
        searchApi();
    }
});