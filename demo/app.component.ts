import {Component, OnInit, ViewEncapsulation} from '@angular/core';
import * as shape from 'd3-shape';
import {Subject} from 'rxjs';
import {colorSets} from '../src/utils/color-sets';
import {id} from '../src/utils/id';
import chartGroups from './chartTypes';
import html2canvas from '../node_modules/html2canvas/dist/html2canvas.js';
import {countries, generateHierarchialGraph, getTurbineData, testGraph} from './data';
import {HttpClient, HttpHeaders} from "@angular/common/http";

@Component({
  selector: 'app',
  encapsulation: ViewEncapsulation.None,
  styleUrls: ['./app.component.scss'],
  templateUrl: './app.component.html'
})
export class AppComponent implements OnInit {
  version = APP_VERSION;

  theme = 'dark';
  chartType = 'directed-graph';
  chartTypeGroups: any;
  chart: any;
  realTimeData: boolean = false;
  countrySet: any[];
  graph: { links: any[]; nodes: any[] };
  hierarchialGraph: { links: any[]; nodes: any[] };

  view: any[];
  width: number = 700;
  height: number = 300;
  fitContainer: boolean = true;
  autoZoom: boolean = false;
  panOnZoom: boolean = true;
  enableZoom: boolean = true;
  autoCenter: boolean = false;

  // observables
  update$: Subject<any> = new Subject();
  center$: Subject<any> = new Subject();
  zoomToFit$: Subject<any> = new Subject();

  // options
  showLegend = false;
  orientation: string = 'TB'; // LR, RL, TB, BT

  orientations: any[] = [
    {
      label: 'Stanga la Dreapta',
      value: 'LR'
    },
    {
      label: 'Dreapta la Stanga',
      value: 'RL'
    },
    {
      label: 'Sus in Jos',
      value: 'TB'
    },
    {
      label: 'Jos in Sus',
      value: 'BT'
    }
  ];

  nodes = [{
    id: 'root',
    label: 'root'
  }];
  links = [];
  id = 0;


  // line interpolation
  curveType: string = 'Linear';
  curve: any = shape.curveLinear;
  interpolationTypes = [
    'Bundle',
    'Cardinal',
    'Catmull Rom',
    'Linear',
    'Monotone X',
    'Monotone Y',
    'Natural',
    'Step',
    'Step After',
    'Step Before'
  ];

  testJson: any;

  // testJson = {
  //   "nessuno": {
  //     "?c": {
  //       "?b": {
  //         "Empty Alpha Memory": {}
  //       }
  //     }
  //   },
  //   " alcuni": {
  //     "?a": {
  //       "?c": {
  //         "Empty Alpha Memory": {}
  //       }
  //     }
  //   },
  //   " tutti": {
  //     "?b": {
  //       "?c": {
  //         "Empty Alpha Memory": {}
  //       }
  //     },
  //     "?a": {
  //       "?b": {
  //         "Empty Alpha Memory": {}
  //       }
  //     }
  //   }
  // };

  colorSchemes: any;
  colorScheme: any;
  schemeType: string = 'ordinal';
  selectedColorScheme: string;

  folder = 'Social';
  folder2 = 'test';
  step = 1;
  step2 = 1;
  sursa: any;

  socialImages = [
    {id: 1, url: "https://i.imgur.com/7H7QA07.png"},
    {id: 2, url: "https://imgur.com/0B0EKHN.png"},
    {id: 3, url: "https://imgur.com/PgJO5qM.png"},
    {id: 4, url: "https://imgur.com/FiK1tqw.png"},
    {id: 5, url: "https://imgur.com/S5Fx7ah.png"},
    {id: 6, url: "https://imgur.com/8vjuW7F.png"},
    {id: 7, url: "https://i.imgur.com/CJyHA3n.jpg"},
    {id: 8, url: "https://i.imgur.com/RyU4ILs.jpg"},
    {id: 9, url: "https://imgur.com/NdnJ5CV.png"},
    {id: 10, url: "https://i.imgur.com/LxO65yP.jpg"},
    {id: 11, url: "https://i.imgur.com/KaCCDjj.jpg"},
    {id: 12, url: "https://i.imgur.com/7Su0505.jpg"}
    ];

  socialImages2 = [
    {id: 1, url: "https://i.imgur.com/fVBgVlv.jpg"},
    {id: 2, url: "https://i.imgur.com/WbE79xC.jpg"},
    {id: 3, url: "https://imgur.com/639QtaG.jpg"},
    {id: 4, url: "https://i.imgur.com/LfMBHs1.jpg"},
    {id: 5, url: "https://i.imgur.com/Wfn0RQ5.jpg"}
  ];

  constructor(private http: HttpClient) {
    Object.assign(this, {
      countrySet: countries,
      colorSchemes: colorSets,
      chartTypeGroups: chartGroups,
      hierarchialGraph: generateHierarchialGraph()
    });

    this.setColorScheme('picnic');
    this.setInterpolationType('Bundle');
  }

  ngOnInit() {
    this.selectChart(this.chartType);

    setInterval(this.updateData.bind(this), 1000);

    if (!this.fitContainer) {
      this.applyDimensions();
    }

    this.importValues();
    // console.log(Object.keys(keys[1]));
  }

  // print() {
  //   html2canvas('chart-col').then(function(canvas) {
  //     document.body.appendChild(canvas);
  //   });
  // }

  importValues() {
    // console.log(this.testJson);

    console.log(this.testJson);
    let values = Object.values(this.testJson);
    let keys = Object.keys(this.testJson);
    for (let i in values) {
      this.links.push({source: 'root', target: keys[i].replace(/\s/g, '')});

      let ok = true;
      for (let j = 0; j < this.nodes.length; j++) {
        if (this.nodes[j].label == keys[i].replace(/\s/g, ''))
          ok = false;
      }
      if (ok) {
        this.nodes.push({id: keys[i].replace(/\s/g, ''), label: keys[i].replace(/\s/g, '')});
      }
      this.insertNodesLinks(values[i], keys[i].replace(/\s/g, ''));
    }
  }

  insertNodesLinks(valuesArray, parent) {
    // console.log(valuesArray);
    // console.log(valuesArray.length);
    let values = Object.values(valuesArray);
    let keys = Object.keys(valuesArray);

    for (let i in values) {
      this.links.push({source: parent, target: keys[i].replace(/\s/g, '')});
      let ok = true;
      for (let j = 0; j < this.nodes.length; j++) {
        if (this.nodes[j].label == keys[i].replace(/\s/g, ''))
          ok = false;
      }
      if (ok) {
        this.nodes.push({id: keys[i].replace(/\s/g, ''), label: keys[i].replace(/\s/g, '')});
      }
      this.insertNodesLinks(values[i], keys[i].replace(/\s/g, ''));
      this.showFinal();
    }
  }

  showFinal() {
    this.hierarchialGraph.nodes = [];
    this.hierarchialGraph.links = [];
    this.hierarchialGraph.nodes = this.nodes;
    this.hierarchialGraph.links = this.links;
  }

  downloadPhoto() {
    this.sursa = "images/Social/RETE" + this.step + ".png";
    for(let i = 0; i < this.socialImages.length; i++) {
      if(this.socialImages[i].id == this.step)
        window.open(this.socialImages[i].url,'_blank');

    }
    // window.location.href = "./images/Social/RETE" + this.step + ".png";
  }

  getDetails() {
    this.nodes = [{
      id: 'root',
      label: 'root'
    }];
    this.links = [];
    this.hierarchialGraph.nodes = [];
    this.hierarchialGraph.links = [];

    let Headers = new HttpHeaders();

    Headers.set('Access-Control-Allow-Origin', '*');
    Headers.set('access-control-allow-credentials', 'true');
    Headers.set('Access-Control-Allow-Headers', 'session-variable');
    Headers.set('Access-Control-Allow-Methods', 'GET, OPTIONS');
    Headers.set('vary', 'Origin');

    this.http.get("http://localhost:8080/clips/facts" + "?folder=" + this.folder + "&step=" + this.step, {headers: Headers})
      .subscribe((response: Response) => {
        this.testJson = response;
        this.importValues();
      });

  }

  getDetails2() {
    this.nodes = [{
      id: 'root',
      label: 'root'
    }];
    this.links = [];
    this.hierarchialGraph.nodes = [];
    this.hierarchialGraph.links = [];

    let Headers = new HttpHeaders();

    Headers.set('Access-Control-Allow-Origin', '*');
    Headers.set('access-control-allow-credentials', 'true');
    Headers.set('Access-Control-Allow-Headers', 'session-variable');
    Headers.set('Access-Control-Allow-Methods', 'GET, OPTIONS');
    Headers.set('vary', 'Origin');

    this.http.get("http://localhost:8080/clips/facts" + "?folder=" + this.folder2 + "&step=" + this.step2, {headers: Headers})
      .subscribe((response: Response) => {
        this.testJson = response;
        this.importValues();
      });

  }

  downloadPhoto2() {
    for(let i = 0; i < this.socialImages2.length; i++) {
      if(this.socialImages2[i].id == this.step2)
        window.open(this.socialImages2[i].url,'_blank');

    }
    // window.location.href = "./images/Social/RETE" + this.step + ".png";
  }

  updateData() {
    if (!this.realTimeData) {
      return;
    }

    const country = this.countrySet[Math.floor(Math.random() * this.countrySet.length)];
    const add = Math.random() < 0.7;
    const remove = Math.random() < 0.5;

    if (add) {
      // directed graph

      const hNode = {
        id: id(),
        label: country
      };

      this.hierarchialGraph.nodes.push(hNode);

      this.hierarchialGraph.links.push({
        source: this.hierarchialGraph.nodes[Math.floor(Math.random() * (this.hierarchialGraph.nodes.length - 1))].id,
        target: hNode.id,
        label: 'on success'
      });

      this.hierarchialGraph.links = [...this.hierarchialGraph.links];
      this.hierarchialGraph.nodes = [...this.hierarchialGraph.nodes];
    }
  }

  applyDimensions() {
    this.view = [this.width, this.height];
  }

  toggleEnableZoom(enableZoom: boolean) {
    this.enableZoom = enableZoom;
  }

  toggleFitContainer(fitContainer: boolean, autoZoom: boolean, autoCenter: boolean): void {
    this.fitContainer = fitContainer;
    this.autoZoom = autoZoom;
    this.autoCenter = autoCenter;

    if (this.fitContainer) {
      this.view = undefined;
    } else {
      this.applyDimensions();
    }
  }

  selectChart(chartSelector) {
    this.chartType = chartSelector;

    for (const group of this.chartTypeGroups) {
      for (const chart of group.charts) {
        if (chart.selector === chartSelector) {
          this.chart = chart;
          return;
        }
      }
    }
  }

  select(data) {
    console.log('Item clicked', data);
  }

  setColorScheme(name) {
    this.selectedColorScheme = name;
    this.colorScheme = this.colorSchemes.find(s => s.name === name);
  }

  setInterpolationType(curveType) {
    this.curveType = curveType;
    if (curveType === 'Bundle') {
      this.curve = shape.curveBundle.beta(1);
    }
    if (curveType === 'Cardinal') {
      this.curve = shape.curveCardinal;
    }
    if (curveType === 'Catmull Rom') {
      this.curve = shape.curveCatmullRom;
    }
    if (curveType === 'Linear') {
      this.curve = shape.curveLinear;
    }
    if (curveType === 'Monotone X') {
      this.curve = shape.curveMonotoneX;
    }
    if (curveType === 'Monotone Y') {
      this.curve = shape.curveMonotoneY;
    }
    if (curveType === 'Natural') {
      this.curve = shape.curveNatural;
    }
    if (curveType === 'Step') {
      this.curve = shape.curveStep;
    }
    if (curveType === 'Step After') {
      this.curve = shape.curveStepAfter;
    }
    if (curveType === 'Step Before') {
      this.curve = shape.curveStepBefore;
    }
  }

  onLegendLabelClick(entry) {
    console.log('Legend clicked', entry);
  }

  toggleExpand(node) {
    console.log('toggle expand', node);
  }

  updateChart() {
    this.update$.next(true);
  }

  zoomToFit() {
    this.zoomToFit$.next(true);
  }

  center() {
    this.center$.next(true);
  }
}
