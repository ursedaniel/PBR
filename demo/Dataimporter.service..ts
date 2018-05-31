import {Injectable} from '@angular/core';
import * as Http from "http";

@Injectable()
export class DataimporterService {

  private headers = new Headers({'Content-Type': 'application/json'});
  private search: URLSearchParams;

  private url =  "http://localhost:8080/clips/facts";

  constructor(private http: Http) {
    this.http = http;
  }

  getAuthorityInfo(folder, step) {
    return this.http.get(this.url + "?folder=" + folder + "&step=" + step)
      .map((response: Response) => response.json());
  }

}