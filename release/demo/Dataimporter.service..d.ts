import { Http } from "@angular/http";
export declare class DataimporterService {
    private http;
    private headers;
    private search;
    private url;
    constructor(http: Http);
    getAuthorityInfo(folder: any, step: any): any;
}
