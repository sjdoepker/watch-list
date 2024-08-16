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
                    const entryId = parseInt(strEntryId, 10);
                    if (target.classList.contains("mark-watched-btn")) {
                        this.markAsWatched(entryId, row);
                    }
                    else if (target.classList.contains("delete-btn")){
                        this.deleteEntry(entryId, row);
                    }
                }
            }
        }
    }

}


function entryMarkAsWatched(entryId)
{
    fetch(`entry/update/watched/"${entryId}`)
}
