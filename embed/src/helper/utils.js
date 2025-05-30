
import dayjs from 'dayjs';


export function getDatebyTimestamp(timestamp) {
    const format = "YYYY-MM-DD";
    const today = dayjs();
    const current = dayjs();

    switch (timestamp) {
        case "today":
            return today.format(format);
        case "previous_working_day":
            return current.subtract(1, "day").format(format);
        case "start_mtd":
            return current.startOf("month").format(format);
        case "end_mtd":
            return current.endOf("month").format(format);
        case "start_current_mtd":
            return today.startOf("month").format(format);
        case "end_current_mtd":
            return today.endOf("month").format(format);
        case "start_ytd":
            return current.startOf("year").format(format);
        case "end_ytd":
            return current.endOf("year").format(format);
        default:
            return today.format(format);
    }
}
export function getServerReportDefaultFilter(filter) {
    let fitlers = []
      Object.entries(filter).forEach(([key, value]) => {
          if (
              [
                  "current_working_date",
                  "today",
                  "start_mtd",
                  "end_mtd",
                  "start_current_mtd",
                  "end_current_mtd",
                  "start_ytd",
                  "end_ytd"
              ].includes(value)
          ) {
            fitlers.push({name:key,values:[ getDatebyTimestamp(value)]})
            
          }else if (value=="current_outlet"){
            fitlers.push({name:key,values:[""]})
          }else {
            fitlers.push({name:key,values:[value]})
          }
  
          
      });
      
      return fitlers;
  }
  