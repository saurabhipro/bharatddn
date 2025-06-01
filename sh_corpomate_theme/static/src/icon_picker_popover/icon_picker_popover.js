/** @odoo-module **/
import { Component, useState, useRef, onWillStart, onMounted } from "@odoo/owl";
import { useAutofocus, useService } from "@web/core/utils/hooks";
import { fuzzyLookup } from "@web/core/utils/search";
import { loadBundle } from "@web/core/assets";

export const loader = {
    loadIcon: () => loadBundle("sh_corpomate_theme.assets_icon"),
};

export async function loadIcon() {
    try {
        await loader.loadIcon();
        return odoo.loader.modules.get("@sh_corpomate_theme/icon_picker_popover/icon_picker_popover_data");
    } catch {
        return { icons: [] };
    }
}

export const ICON_PER_ROW = 4

export class IconPickerPopover extends Component {
    static template = "sh_font_awesome_icon_picker_widget.IconPickerPopover";

    static props = ["close?", "onClose?", "onSelect", "state?"];

    setup() {
        this.iconRef = useRef("icon-grid");
        this.ui = useState(useService("ui"));
        useAutofocus()
        this.state = useState({
            activeIconIndex: 0,
            searchTerm: "",
        })
        onWillStart(async () => {
            const { icons } = await loadIcon();
            this.icons = icons;
        });

        onMounted(() => {
            if (this.icons.length === 0) {
                return;
            }
            if (this.props?.state?.currentIcon) {
                const getElement = () => this.iconRef?.el.querySelector(`.sh-Icon[data-icon-class="${this.props?.state?.currentIcon}"`);
                const elem = getElement();
                if (elem) {
                    this.state.activeIconIndex = elem.dataset?.index !== undefined && !isNaN(elem.dataset?.index) ? parseInt(elem.dataset.index) : 0
                    elem.scrollIntoView();
                }
            }

        });
    }
    get iconPerRow(){
        return ICON_PER_ROW
    }
    get searchTerm() {
        return this.props.state ? this.props.state.searchTerm : this.state.searchTerm;
    }

    set searchTerm(value) {
        if (this.props.state) {
            this.props.state.searchTerm = value;
        } else {
            this.state.searchTerm = value;
        }
    }
    get itemsNumber() {
        return this.getIcons().length;
    }

    scrollToIcon(){
        const getElement = () => this.iconRef?.el.querySelector(`.sh-Icon[data-index="${this.state.activeIconIndex}"`);
        const elem = getElement();
        if (elem) {
            elem.scrollIntoView();
        }
    }
    onKeydown(ev) {
        switch (ev.key) {
            case "ArrowUp": {
                const newIndex = this.state.activeIconIndex - ICON_PER_ROW;
                if (newIndex >= 0) {
                    this.state.activeIconIndex = newIndex;
                    this.scrollToIcon();
                }
                break;
            }
            case "ArrowDown": {
                const newIndex = this.state.activeIconIndex + ICON_PER_ROW;
                if (newIndex < this.itemsNumber) {
                    this.state.activeIconIndex = newIndex;
                    this.scrollToIcon();
                }
                break;
            }
            case "ArrowRight": {
                if (this.state.activeIconIndex + 1 === this.itemsNumber) {
                    break;
                }
                this.state.activeIconIndex++;
                this.scrollToIcon();
                ev.preventDefault();
                break;
            }
            case "ArrowLeft": {
                const newIndex = Math.max(this.state.activeIconIndex - 1, 0);
                if (newIndex !== this.state.activeIconIndex) {
                    this.state.activeIconIndex = newIndex;
                    this.scrollToIcon();
                    ev.preventDefault();
                }
                break;
            }
            case "Enter":
                ev.preventDefault();
                this.iconRef.el
                    .querySelector(
                        `.sh-IconPicker-content .sh-Icon[data-index="${this.state.activeIconIndex}"]`
                    )
                    .click();
                break;
            case "Escape":
                this.props.close?.();
                this.props.onClose?.();
                ev.stopPropagation();
        }
    }
    getRowsOfIcons() {
        const icons = this.getIcons();
        let rowsOfIcons = [],
            subIcons = [];
        if (icons.length){
            for (let i = 0; i < icons.length; i++) {
                if (subIcons.length < 5) {
                    subIcons.push(icons[i])
                }
                if (subIcons.length === ICON_PER_ROW || i === icons.length - 1) {
                    rowsOfIcons.push(subIcons);
                    subIcons = [];
                }
            }
        }
        return rowsOfIcons
    }
    getIcons() {
        if (this.searchTerm.length > 1) {
            return fuzzyLookup(this.searchTerm, this.icons, (icon) =>
                [icon.title, ...icon.searchTerms,].join(" ")
            );
        }
        return this.icons;
    }

    selectIcon(ev) {
        let iconClass = ev.currentTarget.dataset?.iconClass;
        this.props.onSelect(iconClass);
    }
}