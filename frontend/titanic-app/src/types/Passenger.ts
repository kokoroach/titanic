export interface Passenger {
  passenger_id: number;
  survived: boolean;
  p_class: number;
  name: string;
  sex: string;
  age: number;
  sib_sp: number;
  par_ch: number;
  ticket: string;
  fare: number;
  cabin: string | null;
  embarked: string;
}