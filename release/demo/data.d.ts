export declare const countries: string[];
export declare function generateGraph(nodeCount: number): {
    links: any[];
    nodes: any[];
};
export declare function generateHierarchialGraph(): {
    links: {
        source: string;
        target: string;
    }[];
    nodes: ({
        id: string;
        label: string;
        rank?: undefined;
        color?: undefined;
    } | {
        id: string;
        label: string;
        rank: string;
        color: string;
    })[];
};
export declare function testGraph(): {
    links: {
        source: string;
        target: string;
    }[];
    nodes: ({
        id: string;
        label: string;
        rank?: undefined;
        color?: undefined;
    } | {
        id: string;
        label: string;
        rank: string;
        color: string;
    } | {
        id: string;
        label: string;
        color: string;
        rank?: undefined;
    })[];
};
export declare function getTurbineData(): {
    nodes: any[];
    links: any[];
};
