/** @odoo-module **/

import { OdooEditor } from "@web_editor/js/editor/odoo-editor/src/OdooEditor";
import * as OdooEditorLib from "@web_editor/js/editor/odoo-editor/src/OdooEditor";


import { patch } from "@web/core/utils/patch";
const {
    closestBlock,
    commonParentGet,
    containsUnremovable,
    DIRECTIONS,
    endPos,
    ensureFocus,
    getCursorDirection,
    getFurthestUneditableParent,
    getListMode,
    getOuid,
    insertText,
    isColorGradient,
    nodeSize,
    preserveCursor,
    setCursorStart,
    setSelection,
    startPos,
    toggleClass,
    closestElement,
    isVisible,
    isHtmlContentSupported,
    rgbToHex,
    isFontAwesome,
    ICON_SELECTOR,
    getInSelection,
    getDeepRange,
    getRowIndex,
    getColumnIndex,
    ancestors,
    firstLeaf,
    previousLeaf,
    nextLeaf,
    isUnremovable,
    fillEmpty,
    isEmptyBlock,
    URL_REGEX,
    isSelectionFormat,
    YOUTUBE_URL_GET_VIDEO_ID,
    unwrapContents,
    peek,
    rightPos,
    getAdjacentPreviousSiblings,
    getAdjacentNextSiblings,
    isBlock,
    getTraversedNodes,
    getSelectedNodes,
    descendants,
    hasValidSelection,
    hasTableSelection,
    pxToFloat,
    parseHTML,
    splitTextNode,
    isEditorTab,
    isMacOS,
    isProtected,
    isArtificialVoidElement,
    cleanZWS,
    isZWS,
    setCursorEnd,
    paragraphRelatedElements,
    getDeepestPosition,
    leftPos,
    isNotAllowedContent,
    childNodeIndex,
    EMAIL_REGEX,
    prepareUpdate,
    boundariesOut,
    getFontSizeDisplayValue,
}  = OdooEditorLib;




// import { UNBREAKABLE_ROLLBACK_CODE, UNREMOVABLE_ROLLBACK_CODE } from './utils/constants.js';
/* global DOMPurify */

const BACKSPACE_ONLY_COMMANDS = ['oDeleteBackward', 'oDeleteForward'];
const BACKSPACE_FIRST_COMMANDS = BACKSPACE_ONLY_COMMANDS.concat(['oEnter', 'oShiftEnter']);

// 60 seconds
const HISTORY_SNAPSHOT_INTERVAL = 1000 * 60;
// 10 seconds
const HISTORY_SNAPSHOT_BUFFER_TIME = 1000 * 10;

const KEYBOARD_TYPES = { VIRTUAL: 'VIRTUAL', PHYSICAL: 'PHYSICAL', UNKNOWN: 'UKNOWN' };

export const AVATAR_SIZE = 25;



// Commands that don't require a DOM selection but take an argument instead.
const SELECTIONLESS_COMMANDS = ['addRow', 'addColumn', 'removeRow', 'removeColumn', 'resetSize'];

const EDITABLE_LINK_SELECTOR = 'a:not(.nav-link):not([contenteditable="false"])';

function defaultOptions(defaultObject, object) {
    const newObject = Object.assign({}, defaultObject, object);
    for (const [key, value] of Object.entries(object)) {
        if (typeof value === 'undefined') {
            newObject[key] = defaultObject[key];
        }
    }
    return newObject;
}
function getImageFiles(dataTransfer) {
    return [...dataTransfer.items]
        .filter(item => item.kind === 'file' && item.type.includes('image/'))
        .map((item) => item.getAsFile());
}
function getImageUrl (file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();

        reader.readAsDataURL(file);
        reader.onloadend = (e) => {
            if (reader.error) {
                return reject(reader.error);
            }
            resolve(e.target.result);
        };
    });
}
	




// const OdooEditor = OdooEditorLib.OdooEditor;
// const getDeepRange = OdooEditorLib.getDeepRange;
patch(OdooEditor.prototype, {
    // getPreposition(searchItem) {
    //     let preposition = super.getPreposition(searchItem);
    //     if (this.fields[searchItem.fieldName].name == 'payment_date') {
    //         preposition = _t("until");
    //     }
    //     return preposition
    // }


    _setLinkZws() {
        this._resetLinkZws();
        const selection = this.document.getSelection();
        // ------------------------------------------------    
        // SOFTHEALER CUSTOM CODE HERE
        // SOFTHEALER JUST PUTED BELOW IF CONDITION TO AVOID ERROR
        // ON CHANGE OF READYMADE THEME
        /*
website.backend_assets_all_wysiwyg.min.js:784 Uncaught TypeError: Cannot read properties of null (reading 'isCollapsed')
    at OdooEditor._setLinkZws (website.backend_assets_all_wysiwyg.min.js:784:277)
    at OdooEditor.historyStep (website.backend_assets_all_wysiwyg.min.js:704:162)
    at website.backend_assets_all_wysiwyg.min.js:663:444       
       
        */
        if (selection == undefined || selection == null){
            return;
        }
        // SOFTHEALER CUSTOM CODE ENDS             
        // ------------------------------------------------    

        if (!selection.isCollapsed) {
            return;
        }
        const linkInSelection = getInSelection(this.document, EDITABLE_LINK_SELECTOR);
        const isLinkSelection = selection.anchorNode === linkInSelection;
        let commonAncestorContainer = selection.rangeCount && selection.getRangeAt(0).commonAncestorContainer;
        if (commonAncestorContainer) {
            // Consider all the links in the closest block that contains the
            // whole selection, limiting to the editable.
            if (!this.editable.contains(commonAncestorContainer)) {
                commonAncestorContainer = this.editable;
            }
            let block = closestBlock(commonAncestorContainer);
            if (!block || !this.editable.contains(block)) {
                block = this.editable;
            }
            let links = [...block.querySelectorAll(EDITABLE_LINK_SELECTOR)];
            // Consider the links at the edges of the sibling blocks, limiting
            // to the editable.
            if (this.editable.contains(block)) {
                links.push(
                    closestElement(previousLeaf(block, this.editable, true), EDITABLE_LINK_SELECTOR),
                    closestElement(nextLeaf(block, this.editable, true), EDITABLE_LINK_SELECTOR),
                );
            }
            const offset = selection.anchorOffset;
            let didAddZwsInLinkInSelection = false;
            for (const link of links) {
                if (
                    link &&
                    link.textContent.trim() !== '' &&
                    // Only add the ZWS for simple (possibly styled) text links.
                    ![link, ...link.querySelectorAll('*')].some(isBlock)
                ) {
                    this._insertLinkZws('start', link);
                    // Only add the ZWS at the end if the link is in selection.
                    if (link === linkInSelection) {
                        this._insertLinkZws('end', link);
                        link.classList.add('o_link_in_selection');
                        didAddZwsInLinkInSelection = true;
                    }
                    const zwsAfter = this._insertLinkZws('after', link);
                    if (!zwsAfter.parentElement || !zwsAfter.parentElement.isContentEditable) {
                        zwsAfter.remove();
                    }
                }
            }
            if (isLinkSelection && offset && didAddZwsInLinkInSelection) {
                // Correct the offset if the link is in selection, to account
                // for the added ZWS.
                setSelection(linkInSelection, Math.min(offset + 1, linkInSelection.childNodes.length));
            }
        }
    }



});

