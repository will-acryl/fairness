// 확인용!!
$(document).on('click', '.title', () => {
    console.log(csvData);
});

$(document).ready(function () {
    /*step classname add*/
    if (window.location.pathname == "/data") {
        $(".step-state")[0].classList.add("step1");
        $("#back_btn").hide();
        $("#next_btn").show();
    } else if (window.location.pathname == "/mitigate") {
        $(".step-state")[0].classList.add("step2");
        $("#back_btn").show();
        $("#next_btn").show();
    } else if (window.location.pathname == "/compare") {
        $(".step-state")[0].classList.add("step3");
        $("#back_btn").show();
        $("#next_btn").hide();
        $("#back_btn").css("margin-right", "120px");
    }

    // 라디오 버튼 클릭
    $(".choice").click(function (e) {
        $("input:radio[name='radio-group']").prop("checked", false);
        $(e.currentTarget).siblings().eq(0).prop("checked", true);

        addingAttributeDisplayHandler($('.radio-dataset').index($(e.currentTarget).siblings().eq(0)));
    });

    // 초기에 업로드 방식 기본값
    $('#csvUpload').prop('checked', true)

    // 업로드 방식 변경시 핸들러
    $('.upload-type').change((e) => {
        uploadBtnDisplayHandler($('.upload-type').index(e.target))
    });

    // 업로드 방식 선택 핸들러
    $(".radio-dataset").change((e) => {
        addingAttributeDisplayHandler($('.radio-dataset').index(e.target));
    });

    // 다음번튼 핸들러
    $("#next_btn").click(function (e) {
        // 처음 데이터 선택
        if (window.location.pathname == "/data") {
            let radioVal;

            // csv 파일 업로드 안했을 경우
            if (csvData.substring == '' || csvData.data.length <= 0) {
                radioVal = $("input[name='radio-group']:checked").attr("id");
            }
            else if (csvData.label[getRadioIndex()].length < 3) {
                alert("모두선택")
                return;
            }
            // csv 파일 있을경우
            else {
                csvData.features[getRadioIndex()].push(csvData.label[getRadioIndex()][0])
                radioVal = csvData.name;
                const csvFormData = new FormData();
                csvFormData.append('protect', csvData.protect[getRadioIndex()]);
                csvFormData.append('features', csvData.features[getRadioIndex()]);
                csvFormData.append('optimValue', csvData.optimValue[getRadioIndex()]);
                csvFormData.append('label', csvData.label[getRadioIndex()]);
                callApi('select_attribute_option', 'POST', csvFormData);
            }

            if (radioVal == null) {
                return false;
            }
            $("#select_val").val(radioVal);
            $("#form_tag").submit();
        }

        else if (window.location.pathname == "/mitigate") {
            let radioVal = $("input[name='radio-group']:checked").attr("id");
            if (radioVal == null) {
                alert("");
                return false;
            }
            $("#select_val2").val(radioVal);
            $("#form_tag").submit();
        }
    });

    $("#back_btn").click(function (e) {
        if (window.location.pathname == "/mitigate") {
            $("#form_tag").attr("action", "/data");
        }
        $("#form_tag").submit();
    });
});

// ================데이터 불러오기trevor=======================
let csvData = {
    name: '',
    path: '',
    data: [],
    protect: [[], [], []],
    features: [[], [], []],
    optimValue: [[], [], []],
    label: [[], [], []]
};      //불러온 데이터

// 데이터 선택 alert 닫기 버튼
$(document).on('click', '.close-btn', () => {
    $('#loading_div').css('display', 'flex');

    setTimeout(() => {
        $('.title-sel').empty();
        $('.data-sel').empty();
        $('#csv-alert').css('display', 'none');
        $('#loading_div').css('display', 'none');
    }, 50);
});

// 선택한 항목 확인 버튼
$(document).on('click', '.ok-btn', () => {
    $('#loading_div').css('display', 'flex');

    setTimeout(() => {
        if ($('.title-sel option:selected')[0].index === 0 || $('.data-sel option:selected')[0].index === 0) {
            $('#loading_div').css('display', 'none');
            alert('Please select all items.');
            return;
        }
        const attribute = $('.title-sel option:selected')[0].text;
        const value = $('.data-sel option:selected')[0].text;

        if (isExistenceAttribute(attribute, value, getRadioIndex())) {
            $('#loading_div').css('display', 'none');
            setTimeout(() => { alert('This protective attribute already exists.') }, 50);
            return;
        }

        $('#csv-alert').css('display', 'none');

        csvData.protect[getRadioIndex()].push(attribute);
        csvData.protect[getRadioIndex()].push(value);

        appendAttributes(attribute, value, getRadioIndex());
        $('#loading_div').css('display', 'none');
        $('.title-sel').empty();
        $('.data-sel').empty();
    }, 50);
});

// features 선택 닫기 버튼
$(document).on('click', '.features-close-btn', () => {
    $('.features-list-content').empty();
    $('#csv-features-alert').css('display', 'none');
});

// features 선택 확인 버튼
$(document).on('click', '.features-ok-btn', () => {
    if ($('div.features-list-content input[name=features]:checked').length < 1) {
        alert("please select features.");
        return;
    }

    csvData.features[getRadioIndex()] = [];
    $('div.features-list-content input[name=features]:checked').each((_, featuresElement) => {
        csvData.features[getRadioIndex()].push(featuresElement.value);
    });

    $('#features-list-content').empty();
    $('#csv-features-alert').css('display', 'none');
});

// optim select value 확인 버튼
$(document).on('click', '.optim-ok-btn', () => {
    $('#loading_div').css('display', 'flex');

    setTimeout(() => {
        let optimValue = Array.from(Array(csvData.features[getRadioIndex()].length - 2), () => [])

        $('.feature-attr-item').each((i, elmt) => {
            optimValue[i].splice(0, 0, elmt.innerText)
        })

        $('.feature-value-item').each((i, elmt) => {
            optimValue[i].splice(1, 0, elmt.value)
        })

        $('.feature-value-type-item').each((i, elmt) => {
            optimValue[i].splice(2, 0, elmt.value)
        })

        if (!isOptimItemAllChecked(optimValue)) {
            $('#loading_div').css('display', 'none');
            alert("Please select all items.");
            return;
        }

        csvData.optimValue[getRadioIndex()] = optimValue

        $('#loading_div').css('display', 'none');
        $('#optim-setting-alert').css('display', 'none');
    }, 50);
})

// optim 닫기 버튼
$(document).on('click', '.optim-close-btn', () => {
    $('.optim-list-content').empty();
    $('#optim-setting-alert').css('display', 'none');
});

// label 선택 닫기 버튼
$(document).on('click', '.label-close-btn', () => {
    $('#loading_div').css('display', 'flex');

    setTimeout(() => {
        $('.label-title-sel').empty();
        $('.label-type-sel').empty();
        $('.label-data-sel').empty();
        $('#csv-label-alert').css('display', 'none');
        $('#loading_div').css('display', 'none');
    }, 50);
});

// label 선택 확인 버튼
$(document).on('click', '.label-ok-btn', () => {
    $('#loading_div').css('display', 'flex');

    setTimeout(() => {
        if ($('.label-title-sel option:selected')[0].index === 0 ||
            $('.label-type-sel option:selected')[0].index === 0 ||
            $('.label-data-sel option:selected')[0].index === 0) {
            $('#loading_div').css('display', 'none');
            alert('Please select label.');
            return;
        }
        const attribute = $('.label-title-sel option:selected')[0].text;
        const value = $('.label-data-sel option:selected')[0].text;
        const type = $('.label-type-sel option:selected').val();

        if (isExistenceAttribute_features(attribute, getRadioIndex())) {
            $('#loading_div').css('display', 'none');
            setTimeout(() => { alert('This label already exists.') }, 50);
            return;
        }

        csvData.label[getRadioIndex()] = [];

        $('#csv-label-alert').css('display', 'none');

        csvData.label[getRadioIndex()].push(attribute);
        csvData.label[getRadioIndex()].push(value);
        csvData.label[getRadioIndex()].push(type);

        $('#loading_div').css('display', 'none');
        $('.label-title-sel').empty();
        $('.label-type-sel').empty();
        $('.label-data-sel').empty();
    }, 50);
});

// 데이터 내부 데이터 선택 핸들러
$(document).on('click', '.data-sel', () => {
    if ($('.title-sel option:selected')[0].index === 0) {
        alert("Please select attribute of data first.");
        return;
    }
});

// label data 선택시 title 선택을 안했을 경우
$(document).on('click', '.label-data-sel', () => {
    if ($('.label-title-sel option:selected')[0].index === 0) {
        alert("Please select attribute of data first.");
        return;
    }
});

// label type 선택시 title 선택을 안했을 경우
$(document).on('click', '.label-type-sel', () => {
    if ($('.label-title-sel option:selected')[0].index === 0) {
        alert("Please select attribute of data first.");
        return;
    }
});

// 항목선택
$(document).on('click', '.select-attributes-btn', () => {
    if (
        csvData.name === '' ||
        csvData.data.length <= 0
    ) {
        alert("Please upload csv file.");
        return;
    }

    if (csvData.protect[getRadioIndex()].length >= 4) {
        alert("All protected attributes have been selected.");
        return;
    }

    $('#loading_div').css('display', 'flex');

    setTimeout(() => {
        $('#csv-alert').css('display', 'flex');
        $('.data-sel').append(`<option selected disabled hidden>Choose data</option>`);
        titleSelInput();
    }, 50);
});

// features list 선택
$(document).on('click', '.select-features-btn', () => {
    if (
        csvData.name === '' ||
        csvData.data.length <= 0
    ) {
        alert("Please upload csv file.");
        return;
    }
    if (csvData.protect[getRadioIndex()].length != 4) {
        alert("Please select the protect attribute first.")
        return;
    }
    $('.features-list-content').empty();
    $('#csv-features-alert').css('display', 'flex');

    featuresSelInput();
});

// optim 항목 선택
$(document).on('click', '.select-optim-btn', () => {
    if (csvData.name === '' || csvData.data.length <= 0) {
        alert("Please upload csv file.");
        return;
    }
    if (csvData.protect[getRadioIndex()].length != 4) {
        alert("Please select the protect attribute first.");
        return;
    }
    if (csvData.features[getRadioIndex()].length < 3) {
        alert("Please select features first.");
        return;
    }
    $('#loading_div').css('display', 'flex');


    setTimeout(() => {
        $('.optim-list-content').empty()
        $('#optim-setting-alert').css('display', 'flex');
        optimLabelList = []
        csvData.features[getRadioIndex()].map((d) => {
            if (csvData.protect[getRadioIndex()][0] != d && csvData.protect[getRadioIndex()][2] != d) {
                optimLabelList.push(d)
            }
        });

        optimAttrInput(optimLabelList);
    }, 50);
});

// label 선택
$(document).on('click', '.select-label-btn', () => {
    if (csvData.name === '' || csvData.data.length <= 0) {
        alert("Please upload csv file.");
        return;
    }
    if (csvData.protect[getRadioIndex()].length != 4) {
        alert("Please select the protect attribute first.");
        return;
    }
    if (csvData.features[getRadioIndex()].length < 3) {
        alert("Please select features first.");
        return;
    }
    if (csvData.optimValue[getRadioIndex()].length != csvData.features[getRadioIndex()].length - 2) {
        alert("Please select optim value first.");
        return;
    }
    $('#loading_div').css('display', 'flex');

    setTimeout(() => {
        $('#csv-label-alert').css('display', 'flex');
        $('.label-type-sel').append(`<option selected disabled hidden>Choose type</option>`);
        $('.label-data-sel').append(`<option selected disabled hidden>Choose data</option>`);
        labelTitleSelInput();
    }, 50);
});

// 데이터 타이틀 선택 핸들러
$(document).on('change', '.title-sel', () => {
    $('#loading_div').css('display', 'flex');
    $('.data-sel').empty();
    $('.data-sel').append(`<option selected disabled hidden>Choose data</option>`);
    setTimeout(() => dataSelInput(parseInt($('.title-sel option:selected')[0].index - 1)), 50);
});

// 라벨 선택 핸들러
$(document).on('change', '.label-title-sel', () => {
    $('#loading_div').css('display', 'flex');
    $('.label-type-sel').empty();
    $('.label-data-sel').empty();
    $('.label-type-sel').append(`<option selected disabled hidden>Choose type</option>`);
    $('.label-data-sel').append(`<option selected disabled hidden>Choose data</option>`);
    setTimeout(() => {
        labelDataSelInput(parseInt($('.label-title-sel option:selected')[0].index - 1))
        labelTypeSelInput($('.label-title-sel').val(), parseInt($('.label-title-sel option:selected')[0].index - 1))
    }, 50);
});

// attributes 삭제
$(document).on('click', '.protected-data-del-btn', (e) => {
    const attrValue = $(e.currentTarget).parent().attr('value').split('|');
    let idx;

    for (let i = 0; i < 4; i += 2) {
        if (attrValue[0] === csvData.protect[getRadioIndex()][i] && attrValue[1] === csvData.protect[getRadioIndex()][i + 1]) {
            idx = i;
        }
    }

    // const idx = csvData.protect[getRadioIndex()].findIndex((item) => {
    //   return (item.attribute === attrValue[0] && item.value === attrValue[1]);
    // });

    csvData.protect[getRadioIndex()].splice(idx, idx + 2);

    $(e.currentTarget).parent().remove();
});

// description 클릭
$(document).on('click', '.protected-attributes-description', () => {
    $('#description-alert').css('display', 'flex');
});

// description 닫기
$(document).on('click', '.description-close-btn', () => {
    $('#description-alert').css('display', 'none');
});

// 로컬csv upload
$(document).on('click', '.csv-send-btn', () => {
    if ($('#csv-input').val() === "") {
        alert("Please select csv file.")
        return;
    }

    const csvFormData = new FormData();
    csvFormData.append('csvFile', $('#csv-input').prop('files')[0]);
    $('#loading_div').css('display', 'flex');

    setTimeout(() => {
        callApi('uploadCSV', 'POST', csvFormData);
    }, 50);
});

// url로 csv upload
$(document).on('click', '.csv-upload-btn.upload-url', () => {
    if ($('#url-csv-input').val() === "" || $('#fileName-csv-input').val() === "") {
        alert("Please enter csv url and file name.")
        return;
    }

    $('.protected-attributes-content').empty();

    const csvFormData = new FormData();
    csvFormData.append('url', $('#url-csv-input').val())
    csvFormData.append('filename', $('#fileName-csv-input').val())

    $('#loading_div').css('display', 'flex');

    setTimeout(() => {
        callApi('uploadUrlCSV', 'POST', csvFormData)
    }, 50)
});

// -------event end--------
// 데이터 로드
function loadFile(sender) {
    if (sender.value === '') return;

    $('.protected-attributes-content').empty();
}

// api요청 함수
const callApi = (url, type, csvFormData) => {
    $.ajax({
        url: url,
        type: type,
        enctype: 'multipart/form-data',
        data: csvFormData,
        contentType: false,
        processData: false,
        async: false,
        cache: false,
        success: url === "uploadCSV" || url === "uploadUrlCSV" ? successCSV : successAttr,
        error: error
    });
};

// api 요청 성공시
const successCSV = (result) => {
    $('#loading_div').css('display', 'none');
    $('.uploaded-txt').css('display', 'flex');
    result = eval("(" + result + ")");

    csvData.name = result["csvName"]
    csvData.data = result["csvFile"]

    csvData.data.map((d) => {
        if (csvData.data[0].length != d.length) {
            alert("There may be an error due to an empty item. please check your dataset.")
        }
    })
};

// api 
const successAttr = (result) => {

}

// api요청 실패시
const error = (request, error) => {
    $('#loading_div').css('display', 'none');
    $('.uploaded-txt').css('display', 'none');

    alert("There was an error in the process of uploading the file. please check your dataset.");
}

// 불러온 데이터 타이틀 옵션 추가
const titleSelInput = () => {
    $('.title-sel').append(`<option selected disabled hidden>Choose title</option>`);

    $('.title-sel').append(csvData.data[0].map((data) => {
        return `<option value='${data}' >${data}</option>`;
    }));

    $('#loading_div').css('display', 'none');
};

// features 체크박스 추가
const featuresSelInput = () => {
    $('.features-list-content').append(csvData.data[0].map((data) => {
        return `
      <div class="features-item">
        <input 
          type="checkbox" 
          id="${data}" 
          name="features" 
          value="${data}" 
          ${csvData.features[getRadioIndex()].indexOf(data) != -1 ? "checked" : ""}
          ${csvData.protect[getRadioIndex()][0].indexOf(data) != -1 ? "checked disabled" : ""}
          ${csvData.protect[getRadioIndex()][2].indexOf(data) != -1 ? "checked disabled" : ""}
        />
        <label for="${data}">${data}</label>
      </div>
    `;
    }));
};

// optim attr item 추가
const optimAttrInput = (optimLabelList) => {
    $('.optim-list-content').append(optimLabelList.map((attr) => {
        let values = columnToArray(csvData.data, csvData.data[0].indexOf(attr));
        values = Array.from(new Set(values)).slice(1, values.length);

        return `
            <div class="feature-attr-value-item">
                <li class="feature-attr-item">${attr}</li>
                <select class="feature-value-item">
                    <option selected disabled hidden>Choose data</option>
                    ${optimValueInput(values)}
                </select>
                <select class="feature-value-type-item">
                    <option selected disabled hidden>Choose data</option>
                    ${optimTypeInput(attr, values)}
                </select>
            </div>
        `
    }));

    $('#loading_div').css('display', 'none');
};

// optim value item 추가
const optimValueInput = (values) => {
    let optionList = ``

    if (!isNaN(parseFloat(values[0])) && values.length != 2) {
        values.sort(function (a, b) {
            return a - b;
        })
    }

    optionList += values.map(v => { return `<option value='${v}'>${v}</option>` })

    return optionList
}

// optim type item 추가
const optimTypeInput = (attr, values) => {
    const strLabel = `<option value='='>${attr} = X</option>`
    const numLabel = `
        <option value='>'>${attr} &gt X</option>
        <option value='>='>${attr} &gt= X</option>
        <option value='='>${attr} = X</option>
        <option value='<='>${attr} &lt= X</option>
        <option value='<'>${attr} &lt X</option>
    `

    if (isNaN(parseFloat(values[0])) || values.length === 2) {
        return strLabel;
    }
    else {
        return numLabel;
    }
}

// optim 모든 항목 선택 확인 함수
const isOptimItemAllChecked = (optimValue) => {
    let isAllChecked = true
    optimValue.map((item) => {
        if (item[1] === "Choose data" || item[2] === "Choose data") {
            isAllChecked = false
        }
    })
    return isAllChecked
}

// label title option 추가
const labelTitleSelInput = () => {
    $('.label-title-sel').empty();
    $('.label-type-sel').empty();
    $('.label-data-sel').empty();
    $('.label-title-sel').append(`<option selected disabled hidden>Choose label</option>`)
    $('.label-type-sel').append(`<option selected disabled hidden>Choose type</option>`);
    $('.label-data-sel').append(`<option selected disabled hidden>Choose data</option>`);

    $('.label-title-sel').append(csvData.data[0].map((data) => {
        return `<option value='${data}'>${data}</option>`;
    }));

    $('#loading_div').css('display', 'none');
};

// label data 선택
const labelDataSelInput = (selectedTitle) => {
    let data = columnToArray(csvData.data, selectedTitle);
    data = Array.from(new Set(data)).slice(1, data.length);

    if (!isNaN(parseFloat(data[0])) && data.length != 2) {
        data.sort(function (a, b) {
            return a - b;
        })
    }

    $('.label-data-sel').append(data.map(d => { return `<option value='${d}'>${d}</option>` }));

    $('#loading_div').css('display', 'none');
}

// label type option 추가
const labelTypeSelInput = (labelTitle, selectedTitle) => {
    let data = columnToArray(csvData.data, selectedTitle);
    data = Array.from(new Set(data)).slice(1, data.length);

    if (data.length < 2) {
        labelTitleSelInput();
        alert("The number of items in the selected attribute is low.");
        return;
    }

    const strLabel = `<option value='='>${labelTitle} = X</option>`
    const numLabel = `
    <option value='>'>${labelTitle} &gt X</option>
    <option value='>='>${labelTitle} &gt= X</option>
    <option value='='>${labelTitle} = X</option>
    <option value='<='>${labelTitle} &lt= X</option>
    <option value='<'>${labelTitle} &lt X</option>
  `

    if (isNaN(parseFloat(data[0]))) {
        $('.label-type-sel').append(strLabel);
    }
    else if (data.length === 2) {
        $('.label-type-sel').append(strLabel);
    }
    else {
        $('.label-type-sel').append(numLabel);
    }
};

// 선택된 타이틀의 데이터 옵션 추가
const dataSelInput = (selectedTitle) => {
    let data = columnToArray(csvData.data, selectedTitle);
    data = Array.from(new Set(data)).slice(1, data.length);

    $('.data-sel').append(data.map(d => { return `<option value='${d}'>${d}</option>` }));

    $('#loading_div').css('display', 'none');
};

// 배열 열만 추출
const columnToArray = (arr, n) => arr.map(x => x[n]);


// 선택된 라디오 버튼의 adding protected attributes 활성화
const addingAttributeDisplayHandler = (index) => {
    $(".select-attributes-content").each((i, elmt) => {
        $(elmt).css('display', i === index ? 'flex' : 'none');
    });

    $('.protected-attributes-description').each((i, elmt) => {
        $(elmt).css('display', i === index ? 'flex' : 'none');
    });

    $('.protected-attributes-content').each((i, elmt) => {
        $(elmt).children().children('.protected-data-del-btn').css('display', i === index ? 'flex' : 'none')
    });
};

// 업로드 방식 선택시 버튼 활성화/비활성화
const uploadBtnDisplayHandler = (index) => {
    $('.upload-option').each((i, elmt) => {
        $(elmt).css('display', i === index ? 'flex' : 'none')
    });
};

// option 선택 여부 검사
const isCheckedOptim = () => {
    var notSel = false

    $('.feature-value-item').map((i, elmt) => {
        if (elmt.value === "Choose data") {
            notSel = true
        }
    });

    return !notSel
}

// attribute 중복 검사
const isExistenceAttribute = (attribute, value, index) => {
    let result = false;

    if (csvData.protect[index][0] == attribute && csvData.protect[index][1] == value) {
        result = true;
    }

    return result;
};

// label 중복검사용
const isExistenceAttribute_features = (attribute, index) => {
    let result = false;

    for (let i = 0; i < csvData.features[index].length; i++) {
        if (csvData.features[index][i] === attribute) {
            result = true;
            break;
        }
    }
    return result;
};

// 선택된 라디오 버튼(dataset) index 반환
const getRadioIndex = () => {
    $("input[name='radio-group']:checked").each((i, elmt) => {
        index = $(elmt).index("input[name='radio-group']");
    });

    return index;
};

//보호 속성 그리기
const appendAttributes = (attribute, value, index) => {
    // $('.protected-attributes-content').empty();

    $('.protected-attributes-content').each((i, elmt) => {
        if (i === index) {
            $(elmt).append(`
        <div class="protected-data-box" value=${attribute + '|' + value}>  
          <p class="protected-data-txt">- 
            <span>${attribute}</span>
            , privileged: 
            <span>${value}</span>
            , unprivileged: others
          </p>
          <div class="protected-data-del-btn">X</div>
        </div>
      `);
        }
    });
};
