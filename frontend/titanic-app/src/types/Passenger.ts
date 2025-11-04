export interface Passenger {
  passenger_id: number;
  survived: boolean;
  title: string
  first_name: string
  maiden_name: string
  last_name: string
  nickname: string
  alias: string
  spouse: string
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