//
//
//
//
//
//
// Source URLs:
// https://www.microsoft.com/security/pc-security/password-checker.aspx
// https://www.microsoft.com/security/pc-security/assets/scripts/passwdcheck.js
//
//
//
//
//
//

/* New Password checker script*/
var alpha = "abcdefghijklmnopqrstuvwxyz";
var upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
var upper_punct = "~`!@#$%^&*()-_+=";
var digits = "1234567890";

var totalChars = 0x7f - 0x20;
var alphaChars = alpha.length;
var upperChars = upper.length;
var upper_punctChars = upper_punct.length;
var digitChars = digits.length;
var otherChars = totalChars - (alphaChars + upperChars + upper_punctChars + digitChars);

function GEId(sID) {
    return document.getElementById(sID);
}
function calculateBits(passWord) {
    
    if (passWord.length < 0) {
        //alert("Please supply the password");
        return 0;
    }

    var fAlpha = false;
    var fUpper = false;
    var fUpperPunct = false;
    var fDigit = false;
    var fOther = false;
    var charset = 0;

    //var c=new Array();

    for (var i = 0; i < passWord.length; i++) {
        var char = passWord.charAt(i);

        if (alpha.indexOf(char) != -1)
            fAlpha = true;
        else if (upper.indexOf(char) != -1)
            fUpper = true;
        else if (digits.indexOf(char) != -1)
            fDigit = true;
        else if (upper_punct.indexOf(char) != -1)
            fUpperPunct = true;
        else
            fOther = true;

    }

   
    if (fAlpha)
        charset += alphaChars;
    if (fUpper)
        charset += upperChars;
    if (fDigit)
        charset += digitChars;
    if (fUpperPunct)
        charset += upper_punctChars;
    if (fOther)
        charset += otherChars;

    var bits = Math.log(charset) * (passWord.length / Math.log(2));
    
    //alert(Math.floor(bits));
    return Math.floor(bits);
}

function DispPwdStrength(iN, sHL) {
    if (iN > 4) {
        iN = 4;
    }
    for (var i = 0; i < 5; i++) {
        var sHCR = "pwdChkCon0"; if (i <= iN) {
            sHCR = sHL;
        } if (i > 0) {
            GEId("idSM" + i).className = sHCR;
        }
        GEId("idSMT" + i).style.display = ((i == iN) ? "inline" : "none");
    }
}

function EvalPwdStrength(oF, sP) {
    //alert("start");
    var bits = calculateBits(sP);
    //alert(bits);
    if (bits >= 128) {
        DispPwdStrength(4, 'pwdChkCon4');
    }
    else if (bits < 128 && bits >= 64) {
        DispPwdStrength(3, 'pwdChkCon3');
    }
    else if (bits<64 && bits>=56) {
        DispPwdStrength(2, 'pwdChkCon2');
    }
    else if (bits<56) {
        DispPwdStrength(1, 'pwdChkCon1');
    }
    else {
        DispPwdStrength(0, 'pwdChkCon0');
    }
}