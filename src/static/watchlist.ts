// venturing into javascript was unexpected
interface Entry{
    entry_id: number
    is_watched: boolean
}

class ListManager 
{
    private tableElement: HTMLTableElement

    constructor(tableId: string){
        // create the manager for the table
        this.tableElement = document.getElementById(tableId) as HTMLTableElement;
        if (!this.tableElement){
            throw new Error(`Table with id ${tableId} not found`);
        }
        this.initializeEventListeners();

    }

    private initializeEventListeners(): void
    {
        // addEventListener(event type, (listener: type of thing happening => function to call))
        this.tableElement.addEventListener('click', (e: Event) => this.handleClick(e));
    }

    private handleClick(e: Event): void
    {
        const target = e.target as HTMLElement;
        // 3 equals signs? really?
        if (target && target.tagName === "BUTTON") {
            // tr being "table row", need it to update the UI later
            // closest selects the thing that matches the nearest ancestor
            const row = target.closest("tr");
            if (row) {
                const strEntryId = row.getAttribute("data-entry-id");
                if (strEntryId) {
                    // where more button functionality will go if needed
                    const entryId = parseInt(strEntryId, 10);
                    if (target.classList.contains("mark-watched-btn")) {
                        this.sendRequest("/entry/update/watched/${entryId}", "POST", row, this.updateWatchedStatus);
                    }
                    else if (target.classList.contains("delete-btn")){
                        this.sendRequest("/entry/delete/${entryId}", "POST", row, this.deleteEntry);
                    }
                }
            }
        }
    }

    private async sendRequest(
        url: string, 
        method: string, 
        row: HTMLTableRowElement, 
        successCallback: (row: HTMLTableRowElement) => void): Promise<void> {
            try {
                // csrf token not implemented yet
                const response = await fetch(url, {method:method});
                // const response = await fetch(url, {method, headers:{
                //     "X-CSRFToken": this.getCSRFToken;
                // }})
                if (!response.ok){
                    throw new Error("Failed to send request");
                }
                successCallback(row);
            }
            catch (error) {
                console.error("Error:", error);
                // if it's an error type: display it, otherwise show the string 
                alert(error instanceof Error ? :"Error trying to send request");
            }

    }



}

