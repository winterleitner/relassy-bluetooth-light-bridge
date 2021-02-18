import React, {useEffect, useState} from "react";

export const Light = props => {
    const [blue, setBlue] = useState(0)
    const [white, setWhite] = useState(0)

    useEffect(() => {
        setBlue(props.blue)
        setWhite(props.white)
    }, [props.blue])

    const update = async () =>
    {
        const resp = await fetch(`http://192.168.5.2:5000/light?address=${props.address}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({blue: blue, white: white})
        })

    }


    return <div>
        <div>Name: {props.name}</div>
        <table>
            <thead>
            <tr>
                <th>Blau</th>
                <th>Weiß</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>
                    <input name="blue" type="range" value={blue} min={0} max={255} onChange={e => setBlue(parseInt(e.target.value))} onMouseUp={update}/>
                </td>
                <td>
                    <input name="white" type="range" value={white} min={0} max={255} onChange={e => setWhite(parseInt(e.target.value))} onMouseUp={update}/>
                </td>
            </tr>
            </tbody>
        </table>
    </div>
}