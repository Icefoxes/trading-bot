import { FC, useEffect } from 'react';
import sdk from '@stackblitz/sdk';


export const EditorComponent: FC<{}> = () => {
    const embedProject = () => {
        sdk.embedProject(
            // Payload
            'editor-container',
            {

                files: {
                    'index.html': '<h1></h1?',
                    'index.js': `alert('Woohoo! We can start documenting!')`,
                },

                template: 'javascript',
                title: `My First Docs!`,
                description: `This is an example of my first doc!`,
            },
            {
                height: '100%',
                width: '100%',
                hideNavigation: true,
                view: 'editor',
                showSidebar: true
            }
        );
    }
    useEffect(() => {
        embedProject()
    }, [])
    return <div style={{ width: '100%', height: '100%' }} id='editor-container'></div>
}