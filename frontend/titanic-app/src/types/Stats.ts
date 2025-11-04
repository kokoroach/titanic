export type NumericStats = {
  column: string;
  type: "numeric";
  min: number | null;
  max: number | null;
  avg: number | null;
  count: number;
};

export type CategoricalStats = {
  column: string;
  type: "categorical";
  unique_count: number;
  values: { value: string | null; count: number }[];
};

export type StatsResponse = NumericStats | CategoricalStats;
