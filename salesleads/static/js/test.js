// suma przedziału liczb
function sum(start, end, step) {
    var result = [];
    if (typeof (step) != "number") {
        step = 1;
    }

    if (step < 0) {
        for (var i = start; i >= end; i += step) {
            result.push(i);
        }
    } else if (step > 0) {
        for (var i = start; i <= end; i += step) {
            result.push(i);
        }

    }
    return result;
};


// Odwracanie tablicy
function reverseArray(aList) {
    var newList = [];
    for (var i = aList.length - 1; i >= 0; i--) {
        newList.push(aList[i])
    }
    return newList;

}

Array.prototype.reverseArrayInPlace = function () {
    var newList = [];
    for (var i = this.length - 1; i >= 0; i--) {
        newList.push(this[i])
    }
    return newList;
};

var buttonOne = document.querySelector('.btn.next-step.one');
buttonOne.addEventListener('click', function () {
    var categories = document.querySelectorAll('.categories');
    var checkedCategories = [];
    for (var i = 0; i < categories.length; i++) {
        if (categories[i].checked) {
            checkedCategories.push(categories[i].dataset.id);
        }
    }
});

var institutions = document.querySelectorAll('.institutions')


var categories = stepOne.querySelectorAll('.categories');
var checkedCategories = [];
for (var i = 0; i < categories.length; i++) {
    if (categories[i].checked) {
        checkedCategories.push(categories[i].dataset.id);
    }
    ;
}
;
console.log(checkedCategories)

stepOne.addEventListener("click", function () {
    var checkedCategories = [];
    var categories = document.querySelectorAll('.categories')
    for (var i = 0; i < categories.length; i++) {
        if (catogories[i].checked) {
            checkedCategories.push(categories[i].dataset.id);
        }
    }
    console.log(checkedCategories);
});

